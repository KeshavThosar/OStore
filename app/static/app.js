const qs = (x) => document.querySelector(x)
const qsa = (x) => document.querySelector(x)
const gbid = (x) => document.getElementById(x)

let ACCESS_TOKEN = gbid('access-token').value
let AUTH_HEADER = 'Bearer ' + ACCESS_TOKEN
const LIST_FILES_EVENT = new Event('list-files')
const USER_LOGIN_EVENT = new Event('user-login')
const USER_LOGOUT_EVENT = new Event('user-logout')

const listFilesDiv = gbid('list-files')
const alertMessageDiv = gbid('alert-message-container')
const alertMessageText = gbid('alert-message-text')

window.onload = async () => {
  await init()
  console.log('App loaded')
} 

document.addEventListener('list-files', list_files)

async function init() {
  console.log('Access Token: ', ACCESS_TOKEN)
  document.dispatchEvent(LIST_FILES_EVENT)
}

async function login(email, password){

}

async function register(email, password) {

}

async function list_files(){
  let res = await fetch('/storage/list', {
    headers: {
      authorization: AUTH_HEADER
    }
  })
  
  let items = await res.json()
  console.log(items)
  let content = `
  <table class="table table-bordered">
    <thead>
    <tr>
      <th scope="col">File Name</th>
      <th scope="col">Created On</th>
      <th scope="col">SHA256 Checksum</th>
      <th scope="col">Action</th>
    </tr>
  </thead>
  <tbody>`

  for(let i = 0; i < items.length; i++){
    let {created_on, hash, identifier, name} = items[i]
    content += `
    <tr>
      <td>${name}</td>
      <td>${created_on}</td>
      <td>${hash}</td>
      <td>`
    
    content += `
    <button class="btn btn-success" onclick="download_file('${identifier}', '${name}')">
      <i class="bi bi-download"></i>
    </button>`

    content += `
    <button class="btn btn-danger" onclick="delete_file('${identifier}', '${name}')">
      <i class="bi bi-trash"></i>
    </button>`

    content += `</td></tr>`
  }

  content += `</tbody></table>`
  listFilesDiv.innerHTML = content
}

async function upload_file(){

}

async function download_file(identifier, filename){
  popup('Download Started for '+filename)
  let res = await fetch('/storage/download?id='+identifier, {
    headers: {authorization: AUTH_HEADER}
  })
  let blob = await res.blob()
  let blobUrl =  URL.createObjectURL(blob)
  
  const anchor = document.createElement('a')
  anchor.href = blobUrl
  anchor.download = filename
  
  document.body.appendChild(anchor)
  anchor.click()
  document.body.removeChild(anchor) 
  
  URL.revokeObjectURL(blobUrl) 
}

async function delete_file(identifier, filename){
  cnf_delete = confirm('Delete ' + filename + '?')
  if(cnf_delete == true){
    let req = await fetch('/storage/remove?id='+identifier, {
      method: 'DELETE',
      headers: {authorization: AUTH_HEADER}
    })

    if(req.ok){
      popup(filename+' deleted successfully')
    }
    
    dispatch_list_files()
  }

}

function dispatch_list_files(){
  document.dispatchEvent(LIST_FILES_EVENT)
}

function popup(message){
  alertMessageText.innerHTML = message
  alertMessageDiv.classList.remove('d-none')
  setTimeout(() => alertMessageDiv.classList.add('d-none'), 2000)
}


