
# Video API

This is the first task for HNGx stage five.

I paired myself with frontend devs and completed the API for their chrome task.

## API Reference

#### Get all items

```http
  GET /api/upload
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `file` | `string($binary)` | **Required**.  |

#### Get all recordings

```http
  GET /api/recordings
```

#### Get recent recording

```http
  GET /api/recording/recent
```

## Deployment

To deploy this project run

```bash
uvicorn main:app --reload
```

## Installation

Clone this repo, then

```bash
  cd video-api 
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
```
