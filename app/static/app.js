const qs = (x) => document.querySelector(x)
const qsa = (x) => document.querySelector(x)
const gbid = (x) => document.getElementById(x)

let accessTokenInput = gbid('access-token')
let AUTH_HEADER = 'Bearer ' + accessTokenInput.value
const LIST_FILES_EVENT = new Event('list-files')
const USER_LOGIN_EVENT = new Event('user-login')
const USER_LOGOUT_EVENT = new Event('user-logout')

const listFilesDiv = gbid('list-files')
const alertMessageDiv = gbid('alert-message-container')
const alertMessageText = gbid('alert-message-text')

const loginFormHeading = gbid('login-form-heading')
const loginUsernameInput = gbid('username')
const loginPasswordInput = gbid('password')

window.onload = async () => {
  await init()
  console.log('App loaded')
}

document.addEventListener('list-files', list_files)

async function init() {
  const ACCESS_TOKEN = accessTokenInput.value
  if (ACCESS_TOKEN.length == 0) {
    try {
      await list_files()
    } catch (error) {

    }
  } else {
    hide_login_form()
  }
  console.log('Access Token: ', ACCESS_TOKEN)
  document.dispatchEvent(LIST_FILES_EVENT)
}

gbid('login-form').addEventListener('submit', process_form)
async function process_form(event) {
  event.preventDefault()
  let loginFormRole = loginFormHeading.dataset['role']
  let username = loginUsernameInput.value
  let password = loginPasswordInput.value

  if (loginFormRole == 'login') {
    await login(username, password)
  } else if (loginFormRole == 'register') {
    await register(username, password)
  }

}

async function login(email, password) {
  let req = await fetch('/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: `email=${email}&password=${password}`
  })
  let body = await req.json()
  if (req.status != 200) {
    popup('Invalid username/password')
  } else {
    accessTokenInput.value = body['access_token']
    AUTH_HEADER = 'Bearer ' + accessTokenInput.value
    hide_login_form()
    dispatch_list_files()
  }
}

async function register(email, password) {
  let req = await fetch('/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: `email=${email}&password=${password}`
  })

  if (req.status == 409) {
    popup('User already exists. Try Log In?')
  } else {
    await login(email, password)
  }
}

async function list_files() {
  let req = await fetch('/storage/list', {
    headers: {
      authorization: AUTH_HEADER
    }
  })

  let items = await req.json()
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

  for (let i = 0; i < items.length; i++) {
    let { created_on, hash, identifier, name } = items[i]
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

async function download_file(identifier, filename) {
  popup('Download Started for ' + filename)
  let res = await fetch('/storage/download?id=' + identifier, {
    headers: { authorization: AUTH_HEADER }
  })
  let blob = await res.blob()
  let blobUrl = URL.createObjectURL(blob)

  const anchor = document.createElement('a')
  anchor.href = blobUrl
  anchor.download = filename

  document.body.appendChild(anchor)
  anchor.click()
  document.body.removeChild(anchor)

  URL.revokeObjectURL(blobUrl)
}

async function delete_file(identifier, filename) {
  cnf_delete = confirm('Delete ' + filename + '?')
  if (cnf_delete == true) {
    let req = await fetch('/storage/remove?id=' + identifier, {
      method: 'DELETE',
      headers: { authorization: AUTH_HEADER }
    })

    if (req.ok) {
      popup(filename + ' deleted successfully')
    }

    dispatch_list_files()
  }

}

function dispatch_list_files() {
  document.dispatchEvent(LIST_FILES_EVENT)
}

function popup(message) {
  alertMessageText.innerHTML = message
  alertMessageDiv.classList.remove('d-none')
  setTimeout(() => alertMessageDiv.classList.add('d-none'), 2000)
}

function hide_login_form() {
  // Hides login form, shows dashboard
  gbid('user-auth').classList.add('d-none')
  gbid('files-dashboard').classList.remove('d-none')
}

function show(type) {
  if (type == 'login') {
    gbid('alt-login-message').classList.add('d-none')
    gbid('alt-register-message').classList.remove('d-none')
    loginFormHeading.innerText = 'Login'
    loginFormHeading.dataset['role'] = 'login'
  } else if (type == 'register') {
    gbid('alt-login-message').classList.remove('d-none')
    gbid('alt-register-message').classList.add('d-none')
    loginFormHeading.innerText = 'Register'
    loginFormHeading.dataset['role'] = 'register'

  }
}

gbid('uploadForm').addEventListener('submit', process_upload_form)
async function process_upload_form(event) {
  event.preventDefault()

  const fileInput = gbid('fileInput')
  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('file', file);
  formData.append('filename', file.name);
  popup('Upload in progress')
  let req = await fetch('/storage/add', { 
    method: 'POST', 
    headers: { authorization: AUTH_HEADER }, 
    body: formData 
  })
  let body = await req.json()
  if(req.ok){
    dispatch_list_files()
  }
  popup(body.message)


}