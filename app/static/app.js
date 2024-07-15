const qs = (x) => document.querySelector(x)
const qsa = (x) => document.querySelector(x)
const gbid = (x) => document.getElementById(x)

let ACCESS_TOKEN
const LIST_FILES_EVENT = new Event('list_files')
const USER_LOGIN_EVENT = new Event('user_login')
const USER_LOGOUT_EVENT = new Event('user_logout')

window.onload = async () => {
  await init()
  console.log('App loaded')
} 

document.addEventListener('list_files', list_files)

async function init() {

}

async function login(email, password){

}

async function register(email, password) {

}

async function list_files(){
  // Do not commit this

}

async function upload_file(){

}

async function delete_file(){

}



