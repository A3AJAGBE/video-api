
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

## Setup instruction to run locally

If you choose to **fork** before cloning the project be sure to **use the link from your own repo to clone**.

Clone the project

```bash
  git clone https://github.com/A3AJAGBE/video-api.git
```

Go to the project directory

```bash
  cd video-api
```

Create virtual environment

```bash
  python3 -m venv venv
```

Activate virtual environment

```bash
  source venv/bin/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  uvicorn main:app --reload
```

## Environment Variables

To run this project, you will need to create a .env file and add the environment variable to it.

### Create an openai account and generated your api key

`ScreenAPI`

## More on documentation

Check out a live interactive documentation [here](https://video-api.up.railway.app/api/livedoc). It will allow you interact/test the API with ease.

- Go to the page
- Click on the dropdown button on the right side corner of each requests (POST, GET)
- Click on "Try it now" button, it's on the right side corner as well
- Fill the request body (if any)
- click on "Execute"

## Limitations/Assumptions

- Familiarity with Python
- Familiarity with git and GitHub
- No auth Implementation for the API
- The application was developed on  MacOS
- Knowledge of using the command line interface (CLI)
