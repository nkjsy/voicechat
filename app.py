import time
import os
from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import moviepy.editor as mp
import uvicorn
import speech_to_text, text_to_speech, ai

app = FastAPI()
app.mount("/site", StaticFiles(directory="./static", html=True), name="static")


def delete_file(filepath):
    os.remove(filepath)


@app.post("/inference")
async def infer(audio: UploadFile, background_tasks: BackgroundTasks) -> FileResponse:
    print("received request")
    start_time = time.time()

    # transform audio type from webm to wav
    audio_webm = audio.filename
    try:
        contents = audio.file.read()
        with open(audio_webm, 'wb') as f:
            f.write(contents)
    except Exception:
        print(f"There was an error uploading the file {audio_webm}")
    finally:
        audio.file.close()
    audio_wav = audio_webm.replace('.webm', '.wav')
    clip = mp.AudioFileClip(audio_webm)
    clip.write_audiofile(audio_wav)

    user_text = await speech_to_text.speech_recognize_async_from_file(audio_wav)
    ai_text = await ai.get_response(user_text)

    output_audio_filepath = await text_to_speech.speech_synthesis_to_mp3_file(ai_text)
    background_tasks.add_task(delete_file, output_audio_filepath)
    background_tasks.add_task(delete_file, audio_webm)
    background_tasks.add_task(delete_file, audio_wav)

    print('total processing time:', time.time() - start_time, 'seconds')

    return FileResponse(path=output_audio_filepath, media_type="audio/mpeg")


if __name__ == "__main__":
    uvicorn.run(app, port=9000)
