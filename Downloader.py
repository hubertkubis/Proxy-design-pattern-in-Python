import requests

# Subject interface
class FileDownloader:
    def download(self, file_url):
        pass

# Real subject
class RealFileDownloader(FileDownloader):
    def download(self, file_url):
        # The "self" parameter refers to the current instance of the class.
        # It allows access to the instance's attributes and methods.
        # In this case, it is used to define the behavior of the download() method for the RealFileDownloader class.
        # When called, self.download(file_url) will be specific to the instance of the RealFileDownloader class.
        
        # Send an HTTP GET request to the file URL
        response = requests.get(file_url)
        
        if response.status_code == 200:  # Check if the request was successful (status code 200 means success)
            # Open a file named "downloaded.gif" in write-binary mode and save the response content (file data)
            with open("downloaded.gif", "wb") as file:
                file.write(response.content)
            print("File downloaded successfully as 'downloaded.gif'.")
        else:
            print("Failed to download the file.")

# Proxy
class ProxyFileDownloader(FileDownloader):
    def __init__(self):
        # The __init__ method is a special method in Python classes that is automatically called when an object is created.
        # It is used to initialize the object's attributes and perform any necessary setup.
        # In this case, the __init__ method is defining the initialization behavior for the ProxyFileDownloader class.

        # Create an instance of the RealFileDownloader class and assign it to the 'real_downloader' attribute of the current instance
        self.real_downloader = RealFileDownloader()
        

    def download(self, file_url):
        # The "self" parameter refers to the current instance of the class.
        # In this case, it allows access to the instance's attributes and methods, including is_url_safe() and real_downloader.
        # When called, self.download(file_url) will be specific to the instance of the ProxyFileDownloader class.
        
        # Perform security checks before downloading
        if self.is_url_safe(file_url):
            self.real_downloader.download(file_url)  # Forward the download request to the real downloader
        else:
            print("Unsafe file URL. Download rejected.")

    def is_url_safe(self, file_url):
        # Perform simple security checks on the file URL
        if file_url.startswith("https://") and file_url.endswith(".gif"):  # Check if the URL starts with "https://" and ends with ".gif"
            return True  # If the URL passes the checks, it is considered safe
        return False  # If the URL fails any of the checks, it is considered unsafe

# Client code
def main():
    # Create an instance of the ProxyFileDownloader class
    downloader = ProxyFileDownloader()
    
    # Download the file using the proxy downloader
    # Remember to download only legal files with proper license!
    downloader.download("https://media.tenor.com/AQecc2g8uuAAAAAC/duck-dance.gif")

# Check if the current module is being executed as the main program
if __name__ == "__main__":
    main()

