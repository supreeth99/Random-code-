import axios from 'axios';

const downloadFile = async () => {
  try {
    const response = await axios.post(
      'http://localhost:5000/download',
      {
        path: '/path/to/file', // Adjust as needed
        filename: 'example.txt',
      },
      {
        responseType: 'blob', // Important for handling binary data
      }
    );

    // Create a link element to trigger download
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'example.txt'); // Suggested filename
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (error) {
    console.error('Error downloading file:', error);
  }
};

export default downloadFile;