import axios from 'axios';
import { url } from 'inspector';
import { type } from 'os';
const BASE_URL = "http://localhost:5000";
export default new class FileService {

    async getSegment(index: number) {
        const response = await axios({
            url: `${BASE_URL}/get_segment`,
            method: 'GET',
            responseType: 'blob',
            params: { index }
        });
        const blob = new Blob([response.data], { type: 'audio/wav' });
        const url = window.URL.createObjectURL(blob);
        return url;
    }
    async getSegmentsCount() {
        const res = await axios({
            url: `${BASE_URL}/count_segments`,
            method: 'GET',
            responseType: 'json'
        })
        return res.data.num
    }
    async getChordsFiles() {
        try {
            const res = await axios({
                url: `${BASE_URL}/get_chords_files`,
                method: 'GET',
                responseType: 'json'
            })
            return res.data
        }
        catch (err) {
            throw err;
        }
    }

    async getUserRecording() {
        const response = await axios({
            url: `${BASE_URL}/get_user_rec`,
            method: 'GET',
            responseType: 'blob'
        });
        const blob = new Blob([response.data], { type: 'audio/mpeg' });
        const url = window.URL.createObjectURL(blob);
        return url;
    }
    async getUserChordsFile() {
        try {
            const res = await axios({
                url: `${BASE_URL}/get_user_chords`,
                method: 'GET',
                responseType: 'json'
            })
            return res.data
        }
        catch (err) {
            throw err;
        }
    }

    async getSource(req: string) {
        axios.get(`${BASE_URL}/get_${req}`).then((res: any) => {
            console.log(res.data)
            console.log(typeof (res.data))
            const blob = new Blob([res.data], { type: 'audio/mpeg' });
            const url = window.URL.createObjectURL(blob);
            return url;
        }) 
    }
    
    //     try {
    //         const response = await axios({
    //             url: `${BASE_URL}/get_${req}`,
    //             method: 'GET',
    //             responseType: 'blob'
    //         });
    //         console.log(`${BASE_URL}/get_${req}`)
    //         // Create a new blob object from the binary data
    //         const blob = new Blob([response.data], { type: 'audio/mpeg' });

    //         // Create a URL for the blob object
    //         const url = window.URL.createObjectURL(blob);
    //         console.log(url)
    //         return url;
    //     } catch (error) {
    //         console.error('Error fetching :', error);
    //         throw error;
    // }


    async send(file: any[]) {
        try {
            console.log(file[0])
            let formData = new FormData();
            formData.append('song_file', file[0]);

            const res = await axios.post(BASE_URL + '/upload', formData, { headers: { "Content-Type": "multipart/form-data" } });
            console.log(res.data);
            return res.data; // Return the response data
        } catch (err) {
            console.log("error", err);
            throw err; // Throw the error to be caught by the caller
        }
    }
}
