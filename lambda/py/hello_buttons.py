"""
    Copyright 2018 Amazon.com, Inc. and its affiliates. All Rights Reserved.
    Licensed under the Amazon Software License (the "License").
    You may not use this file except in compliance with the License.
    A copy of the License is located at
      http://aws.amazon.com/asl/
    or in the "license" file accompanying this file. This file is distributed
    on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express
    or implied. See the License for the specific language governing
    permissions and limitations under the License.

    Gadgets Test Skill opens with buttons roll call and asks the user to
    push two buttons. On button one press, she changes the color to red and on
    button two press she changes the color to blue. Then closes. This Skill
    demonstrates how to send directives to, and receive events from, Echo Buttons.
"""

import logging
import json

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.serialize import DefaultSerializer

from ask_sdk_model import (Response, RequestEnvelope)
from ask_sdk_model.interfaces.gadget_controller import SetLightDirective
from ask_sdk_model.interfaces.game_engine import (
    StartInputHandlerDirective, StopInputHandlerDirective)
from ask_sdk_model.services.game_engine import (
    Event, EventReportingType, PatternRecognizer, PatternRecognizerAnchorType,
    Pattern, InputEventActionType, InputEvent
)
from ask_sdk_model.services.gadget_controller import (
    AnimationStep, LightAnimation, SetLightParameters, TriggerEventType
)

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

serializer = DefaultSerializer()

# Define the start input handler directive


def build_start_input_handler_directive():
    return StartInputHandlerDirective(
        timeout=30000,
        recognizers={
            "button_down_recognizer": PatternRecognizer(
                anchor=PatternRecognizerAnchorType.end,
                fuzzy=False,
                pattern=[{"action": InputEventActionType.down}]
            ),
            "button_up_recognizer": PatternRecognizer(
                anchor=PatternRecognizerAnchorType.end,
                fuzzy=False,
                pattern=[{"action": InputEventActionType.up}]
            )},
        events={
            "button_down_event": Event(
                meets=['button_down_recognizer'],
                reports=EventReportingType.matches,
                should_end_input_handler=False
            ),
            "button_up_event": Event(
                meets=['button_up_recognizer'],
                reports=EventReportingType.matches,
                should_end_input_handler=False
            ),
            "timeout": Event(
                meets=['timed out'],
                reports=EventReportingType.history,
                should_end_input_handler=True
            )
        }
    )


def build_stop_input_handler_directive(originating_request_id):
    return StopInputHandlerDirective(
        originating_request_id=originating_request_id
    )


def build_button_idle_animation_directive(target_gadgets, animation):
    return SetLightDirective(
        version=1,
        target_gadgets=target_gadgets,
        parameters=SetLightParameters(
            trigger_event=TriggerEventType.none,
            trigger_event_time_ms=0,
            animations=[animation]
        )
    )


def build_button_up_animation_directive(target_gadgets):
    return SetLightDirective(
        version=1,
        target_gadgets=target_gadgets,
        parameters=SetLightParameters(
            trigger_event=TriggerEventType.buttonUp,
            trigger_event_time_ms=0,
            animations=[LightAnimation(
                repeat=1,
                target_lights=["1"],
                sequence=[
                    AnimationStep(
                        duration_ms=300,
                        color="00FFFF",
                        blend=False
                    )
                ]
            )
            ]
        )
    )


def build_button_down_animation_directive(target_gadgets):
    return SetLightDirective(
        version=1,
        target_gadgets=target_gadgets,
        parameters=SetLightParameters(
            trigger_event=TriggerEventType.buttonDown,
            trigger_event_time_ms=0,
            animations=[LightAnimation(
                repeat=1,
                target_lights=["1"],
                sequence=[
                    AnimationStep(
                        duration_ms=300,
                        color="FFFF00",
                        blend=False
                    )
                ]
            )]
        )
    )


def build_breathe_animation(cycles, color, duration):
    return LightAnimation(
        repeat=cycles,
        target_lights=["1"],
        sequence=[
            AnimationStep(
                duration_ms=1,
                blend=True,
                color="000000"
            ),
            AnimationStep(
                duration_ms=duration,
                blend=True,
                color=color
            ),
            AnimationStep(
                duration_ms=300,
                blend=True,
                color=color
            ),
            AnimationStep(
                duration_ms=300,
                blend=True,
                color="000000"
            )
        ]
    )


intro_animation = LightAnimation(
    repeat=15,
    target_lights=["1"],
    sequence=[
        AnimationStep(
            duration_ms=200,
            blend=True,
            color="000000"
        ),
        AnimationStep(
            duration_ms=300,
            blend=True,
            color="FF0000"
        ),
        AnimationStep(
            duration_ms=300,
            blend=True,
            color="FFFF00"
        ),
        AnimationStep(
            duration_ms=300,
            blend=True,
            color="00FF00"
        ),
        AnimationStep(
            duration_ms=300,
            blend=True,
            color="00FFFF"
        ),
        AnimationStep(
            duration_ms=300,
            blend=True,
            color="0000FF"
        ),
        AnimationStep(
            duration_ms=300,
            blend=True,
            color="FF00FF"
        )
    ]
)


breath_animation_red = build_breathe_animation(30, 'FF0000', 1000)
breath_animation_green = build_breathe_animation(30, '00FF00', 1000)
breath_animation_blue = build_breathe_animation(30, '0000FF', 1000)
animations = [breath_animation_red,
              breath_animation_green, breath_animation_blue]


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    logger.info("launch_request_handler: handling request")

    session_attr = handler_input.attributes_manager.session_attributes
    response_builder = handler_input.response_builder

    # Start keeping track of some state.
    session_attr["button_count"] = 0

    # Preserve the originatingRequestId.  We'll use this to stop the
    # InputHandler later.
    # See the Note at https://developer.amazon.com/docs/gadget-skills/receive-echo-button-events.html#start
    session_attr["current_input_handler_id"] = handler_input.request_envelope.request.request_id

    # On launch, this skill will immediately set up the InputHandler to
    # listen to all attached buttons for 30 seconds.
    # The Skill will then set up two events that each report when buttons are
    # pressed and when they're released.
    # After 30 seconds, the Skill will receive the timeout event.
    # For more details on InputHandlers, see
    # https://developer.amazon.com/docs/gadget-skills/define-echo-button-events.html
    response_builder.add_directive(build_start_input_handler_directive())

    # If the buttons are awake before the Skill starts, the Skill can send
    # animations to all of the buttons by targeting the empty array [].
    # Build the breathing animation that will play immediately.
    response_builder.add_directive(
        build_button_idle_animation_directive([], intro_animation))

    # Build the 'button down' animation for when the button is pressed.
    response_builder.add_directive(build_button_down_animation_directive([]))

    # Build the 'button up' animation for when the button is released.
    response_builder.add_directive(build_button_up_animation_directive([]))

    # Setting should_end_session to None will keep the session open, but NOT open
    # the microphone.
    # You could also set should_end_session to False if you also wanted a
    # voice intent.
    # Never set should_end_session to true if you're expecting InputHandler
    # events Because you'll lose the session!
    # See https://developer.amazon.com/docs/gadget-skills/receive-voice-input.html#types
    response_builder.set_should_end_session(None)

    speech_text = ("Welcome to the Gadgets Test Skill. "
                   "Press your Echo Buttons to change the colors of the lights. "
                   "<audio src='https://s3.amazonaws.com/ask-soundlibrary/foley/amzn_sfx_rhythmic_ticking_30s_01.mp3'/>")

    response_builder.speak(speech_text)

    return response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    logger.info("help_intent_handler: handling request")

    speech_text = ("Welcome to the Gadgets Test Skill. "
                   "Press your Echo Buttons to change the lights. "
                   "<audio src='https://s3.amazonaws.com/ask-soundlibrary/foley/amzn_sfx_rhythmic_ticking_30s_01.mp3'/>")

    return handler_input.response_builder.speak(speech_text).set_should_end_session(None).response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def stop_and_cancel_intent_handler(handler_input):
    """Single handler for Stop and Cancel Intent."""
    # type: (HandlerInput) -> Response
    logger.info("stop_and_cancel_intent_handler: handling request")

    session_attr = handler_input.attributes_manager.session_attributes
    response_builder = handler_input.response_builder

    if "current_input_handler_id" in session_attr and session_attr["current_input_handler_id"] != None:
        response_builder.add_directive(build_stop_input_handler_directive(
            session_attr["current_input_handler_id"]))

    speech_text = "Thank you for using the Gadgets Test Skill. Goodbye."

    return response_builder.speak(speech_text).response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    logger.info("session_ended_request_handler: handling request")
    logger.info("Session ended with reason: " +
                handler_input.request_envelope.request.reason.to_str())
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("GameEngine.InputHandlerEvent"))
def game_engine_input_handler(handler_input):
    """Handler for all game engine events."""
    # type: (HandlerInput) -> Response
    logger.info("game_engine_input_handler: handling request")

    session_attr = handler_input.attributes_manager.session_attributes
    request = handler_input.request_envelope.request
    response_builder = handler_input.response_builder

    game_engine_events = request.events if request.events else []
    for event in game_engine_events:
        button_id = None

        # In this request type, we'll see one or more incoming events that
        # correspond to the StartInputHandler directive we sent above.
        if event.name == "button_down_event":
            button_id = event.input_events[0].gadget_id
            key = button_id + "_initialized"
            is_new_button = False
            if key not in session_attr:
                is_new_button = True
                session_attr["button_count"] = session_attr["button_count"] + 1
                session_attr[key] = True

            if is_new_button:
                button_count = session_attr["button_count"]
                speech_text = (f"Hello button {button_count}. Good to see you. "
                               "<audio src='https://s3.amazonaws.com/ask-soundlibrary/foley/amzn_sfx_rhythmic_ticking_30s_01.mp3'/>")
                response_builder.speak(speech_text)

                # This is a new button, as in new to our understanding.
                # Because this button may have just woken up, it may not have
                # received the initial animations during the launch intent.
                # We'll resend the animations here, but instead of the empty array
                # broadcast above, we'll send the animations ONLY to this buttonId.
                response_builder.add_directive(
                    build_button_idle_animation_directive([button_id], intro_animation))
                response_builder.add_directive(
                    build_button_down_animation_directive([button_id]))
                response_builder.add_directive(
                    build_button_up_animation_directive([button_id]))

            # Again, this means don't end the session, and don't open the microphone.
            response_builder.set_should_end_session(None)
        elif event.name == "button_up_event":
            button_id = event.input_events[0].gadget_id
            key = button_id + "_animation"

            # On releasing the button, we'll replace the 'none' animation
            # with a new color from a set of animations.
            if key in session_attr and session_attr[key] < 2:
                session_attr[key] = session_attr[key] + 1
            else:
                session_attr[key] = 0

            response_builder.add_directive(build_button_idle_animation_directive(
                [button_id], animations[session_attr[key]]))

            # Again, this means don't end the session, and don't open the microphone.
            response_builder.set_should_end_session(None)
        elif event.name == "timeout":
            # The timeout of our InputHandler was reached.  Let's close the Skill session.
            if session_attr["button_count"] == 0:
                response_builder.speak("I didn't detect any buttons. " +
                                       "You must have at least one Echo Button to use this skill.  Goodbye.")
            else:
                response_builder.speak(
                    "Thank you for using the Gadgets Test Skill.  Goodbye.")

    return response_builder.response


@sb.request_handler(can_handle_func=lambda input: True)
def default_handler(handler_input):
    """Handler for all other unhandled requests."""
    # type: (HandlerInput) -> Response
    logger.info("default_handler: handling request")

    speech_text = ("Sorry, I didn't get that. "
                   "Please press your Echo Buttons to change the color of the lights. "
                   "<audio src='https://s3.amazonaws.com/ask-soundlibrary/foley/amzn_sfx_rhythmic_ticking_30s_01.mp3'/>")

    return handler_input.response_builder.speak(speech_text).set_should_end_session(None).response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def error_handler(handler_input, exception):
    """Exception Handler"""
    # type: (HandlerInput, Exception) -> Response
    logger.info("error_handler: handling request")
    logger.error(exception, exc_info=True)

    speech = "Sorry, there was some problem. Please try again!!"
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response


@sb.global_request_interceptor()
def log_request(handler_input):
    """Request Logger"""
    # type: (HandlerInput) -> None
    logger.info("==Request==")
    logger.info(serializer.serialize(handler_input.request_envelope))


@sb.global_response_interceptor()
def log_response(handler_input, response):
    """Response logger."""
    # type: (HandlerInput, Response) -> None
    logger.info("==Response==")
    logger.info(serializer.serialize(response))
    logger.info("==Session Attributes==")
    logger.info(handler_input.attributes_manager.session_attributes)


handler = sb.lambda_handler()
