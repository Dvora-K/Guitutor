import axios from 'axios';
const BASE_URL = "http://localhost:5000";
export default new class FileService {

    // async getPdf() {
    //     try {
    //         const response = await axios({
    //             url: `${BASE_URL}/get_files`,
    //             method: 'GET',
    //             responseType: 'blob'
    //         });
    //         const blob = new Blob([response.data], { type: 'application/pdf' });
    //         console.log(blob.type)
    //         const url = window.URL.createObjectURL(blob);
    //         return url;
    //     } catch (error) {
    //         console.error('Error fetching PDF:', error);
    //         throw error;
    //     }
    // }
    // async getVocal() {
    //     try {
    //         const response = await axios({
    //             url: `${BASE_URL}/get_vocal_drums`,
    //             method: 'GET',
    //             responseType: 'blob'
    //         });
    //         // Create a new blob object from the binary data
    //         const blob = new Blob([response.data], { type: 'audio/wav' });
    //         console.log(blob)
    //         console.log(blob.type)
    //         // Create a URL for the blob object
    //         const url = window.URL.createObjectURL(blob);
    //         return url;
    //     } catch (error) {
    //         console.error('Error fetching vocal:', error);
    //         throw error;
    //     }
    // }

    async getSource(req:string) {
        try {
            const response = await axios({
                url: `${BASE_URL}/get_${req}`,
                method: 'GET',
                responseType: 'blob'
            });
            console.log(`${BASE_URL}/get_${req}`)
            // Create a new blob object from the binary data
            const blob = new Blob([response.data], { type: 'audio/mpeg' });
            console.log(blob)
            console.log(blob.type)
            // Create a URL for the blob object
            const url = window.URL.createObjectURL(blob);
            return url;
        } catch (error) {
            console.error('Error fetching :', error);
            throw error;
        }
    }

    async send(file: any[]) {
        try {
            console.log(file[0])
            let formData = new FormData();
            formData.append('song_file', file[0]);

            const res = await axios.post(BASE_URL + '/upload', formData, { headers: { "Content-Type": "multipart/form-data" } });
            console.log(res.data);
            return res.data; // Return the response data
        } catch (err) {
            console.log(err);
            throw err; // Throw the error to be caught by the caller
        }
    }
}
