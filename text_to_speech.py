import os
import uuid
import azure.cognitiveservices.speech as speechsdk


# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'),
                                       region=os.environ.get('SPEECH_REGION'))

# The language of the voice that responds on behalf of Azure OpenAI.
speech_config.speech_synthesis_voice_name = 'en-US-JennyMultilingualNeural'

# Sets the synthesis output format.
# The full list of supported format can be found here:
# https://docs.microsoft.com/azure/cognitive-services/speech-service/rest-text-to-speech#audio-outputs
speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)


async def speech_synthesis_to_mp3_file(text):
    """performs speech synthesis to a mp3 file"""
    # Creates a speech synthesizer using file as audio output.
    file_name = f"{uuid.uuid4()}.mp3"
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

    result = speech_synthesizer.speak_text_async(text).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}], and the audio was saved to [{}]".format(text, file_name))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    return file_name