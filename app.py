import time
import os
from fastapi import FastAPI, UploadFile, BackgroundTasks, Header
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import speech_to_text, text_to_speech, ai


app = FastAPI()
app.mount("/site", StaticFiles(directory="./static", html=True), name="static")


def delete_file(filepath):
    os.remove(filepath)

# @app.get("/")
# async def hello():
#     print("received get request")
#     return 'par'

@app.post("/inference")
async def infer(audio: UploadFile, background_tasks: BackgroundTasks) -> FileResponse:
    print("received request")
    start_time = time.time()

    user_text = await speech_to_text.speech_recognize_async_from_file(audio.filename)
    ai_text = await ai.get_response(user_text)

    output_audio_filepath = await text_to_speech.speech_synthesis_to_mp3_file(ai_text)
    background_tasks.add_task(delete_file, output_audio_filepath)

    print('total processing time:', time.time() - start_time, 'seconds')

    return FileResponse(path=output_audio_filepath, media_type="audio/mpeg")


if __name__ == "__main__":
    uvicorn.run(app)