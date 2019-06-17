import axios from 'axios'

export default class Api {
    public static getTutorHome(jwt: string) {
        return axios.get('/tutor/home', { headers: { Authorization: `Bearer ${jwt}`}})
    }
    public static getStudentHome(jwt: string) {
        return axios.get('/student/home', { headers: { Authorization: `Bearer ${jwt}`}})
    }
    public static addNewSubject(jwt: string, info: object) {
        return axios.post('/tutor/home', info, { headers: { Authorization: `Bearer ${jwt}`}})
    }
    public static authenticate (userData: any) {  
        return axios.post('/login', userData)
    }
    public static register (type: string, userData: any) {  
        return axios.post(`/register/${type}`, userData)
    }
    public static getCheckpoints(jwt: string, params: any) {
        return axios.get(`/tutor/${params.subject_name}/${params.group_id}/checkpoints`, { headers: { Authorization: `Bearer ${jwt}`}})
    }
    public static addCheckpoints(jwt: string, payload: any) {
        return axios.post(`/tutor/${payload.subject_name}/${payload.group_id}/checkpoints`, 
            { checkpoints: payload.checkpoints },
            { headers: { Authorization: `Bearer ${jwt}`}});
    }
    public static getGradesTable(jwt: string, params: any) {
        return axios.get(`/tutor/${params.subject_name}/${params.group_id}`,
            { headers: { Authorization: `Bearer ${jwt}`}});
    }
    public static updateGradesTable(jwt: string, payload: any) {
        return axios.post(`/tutor/${payload.subject_name}/${payload.group_id}`, 
            payload.newProgress,
            { headers: { Authorization: `Bearer ${jwt}`}});
    }
    public static getProgress(jwt: string, params: any) {
        return axios.get(`/tutor/${params.subject_name}/${params.group_id}/${params.checkpoint_name}`,
            { headers: { Authorization: `Bearer ${jwt}`}});
    }
    public static logout(jwt: string) {
        return axios.post('/logout/access', {}, { headers: { Authorization: `Bearer ${jwt}`}})
    }
}