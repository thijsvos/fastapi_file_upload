# Simple file upload using [FastAPI](https://fastapi.tiangolo.com/)

## Installation

Clone this repo

```
git clone https://github.com/thijsvos/fastapi_file_upload.git
cd fastapi_file_upload
```

Install venv if you haven't already
```
sudo apt-get install python3-pip
python3 -m pip install virtualenv 
```

Create a virtual environment in the `fastapi_file_upload` directory

```
python3 -m venv .
```

Start the `uvicorn` webserver a.k.a. the API
```
python main.py
```

## Usage

Browse to http://localhost:8085/files and enjoy the API.

Optional: use the Powershell commands in the `powershell` file to upload a file. Or use your favourite tool(Postman) to interact with the API.
