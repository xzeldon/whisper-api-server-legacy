# whisper-api-server

### ⚠️ Take a look at the new version of Whisper API Server rewritten in Go! You can find it at [here](https://github.com/xzeldon/whisper-api-server). This updated version eliminates the need for approximately 6GB of Python runtime dependencies.

API server that makes transcription with the OpenAI Whisper models.

```curl
curl http://localhost:8000/v1/audio/transcriptions \
  -H "Content-Type: multipart/form-data" \
  -F file="@/path/to/file/audio.mp3" \
  -F model="whisper-1"
```

```json
{
  "text": "Imagine the wildest idea that you've ever had, and you're curious about how it might scale to something that's a 100, a 1,000 times bigger. This is a place where you can get to do that."
}
```

# About

I made this simple app for [Obsidian voice recognotion](https://github.com/nikdanilov/whisper-obsidian-plugin).
This is working pretty well this usecase. Untested on anything other than Windows.

# Usage

To use this with [Obsidian voice recognotion plugin](https://github.com/nikdanilov/whisper-obsidian-plugin) go to plugin's settings and set

- API KEY = `sk-1`
- API URL = `http://localhost:8000/v1/audio/transcriptions`
- Model = `whisper-1`

An example of using via API is [above](#whisper-api-server).

# Credits

- [This gist](https://gist.github.com/gavrilov/4537a569b7fa8e20e64a199e924d458a) as reference. But I found this implementation a bit slow, especially on every first run (about 30 seconds).
