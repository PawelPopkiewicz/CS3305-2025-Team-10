# Downloading Additional Files
The static files supplied by TFI are too large for GitHub, so you may download the files yourself from the [TFI website](https://www.transportforireland.ie/transitData/PT_Data.html).

# Running a Development Server
Assuming you have the full repository open, use the following command to run the development server.
```py
python -m flask --app back-end/app.py run --debug
```
If you only have the `back-end` subdirectory open, you can run the following command instead.
```py
python -m flask run --debug
```
# Running a Production Server
This is handled by the Docker container.