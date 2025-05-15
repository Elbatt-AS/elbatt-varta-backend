from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

def main():
    # Autentiser med servicekonto - pass på at credentials.json ligger i samme mappe som denne filen
    gauth = GoogleAuth()
    gauth.ServiceAuth()
    drive = GoogleDrive(gauth)

    # Søk etter mappen "Prosjektmappe" (kan endre til mappenavn du ønsker)
    folder_name = "Prosjektmappe"
    folder_list = drive.ListFile({'q': f"mimeType='application/vnd.google-apps.folder' and trashed=false and title='{folder_name}'"}).GetList()

    if not folder_list:
        print(f"Fant ingen mappe med navn '{folder_name}'.")
        return

    for folder in folder_list:
        print(f"Mappe funnet: {folder['title']} med ID: {folder['id']}")

        # List filer i denne mappen
        file_list = drive.ListFile({'q': f"'{folder['id']}' in parents and trashed=false"}).GetList()
        print(f"Filer i mappen '{folder['title']}':")
        for file in file_list:
            print(f" - {file['title']} (ID: {file['id']})")

        # Last opp en testfil til denne mappen
        test_filename = "test_upload.txt"
        with open(test_filename, "w") as f:
            f.write("Dette er en testfil som lastes opp fra script.")

        upload_file = drive.CreateFile({'title': test_filename, 'parents': [{'id': folder['id']}]})
        upload_file.SetContentFile(test_filename)
        upload_file.Upload()
        print(f"Testfil '{test_filename}' lastet opp til mappen '{folder['title']}'.")

        # Fjern lokal testfil
        os.remove(test_filename)

if __name__ == "__main__":
    main()

