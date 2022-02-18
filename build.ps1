.\venv\Scripts\activate
pyinstaller src/wsgi.py -F `
--name "rwp-win-x64" `
--hidden-import waitress `
--paths="/venv/Lib/site-packages/cv2"