const init = () => {
    document.querySelector("#kakao").addEventListener('click', onKakao);
    document.querySelector("#logout").addEventListener('click', onLogout);
    autoLogin();
    redirectPage();
}

const openWindowPopup = (url, name) => {
    var options = 'top=10, left=10, width=500, height=600, status=no, menubar=no, toolbar=no, resizable=no';
    return window.open(url, name, options);
}

const onKakao = async () => {
    document.querySelector("#loading").classList.remove('display_none');

    let url = await fetch("/oauth/url", {
        headers: { "Content-Type": "application/json" },
        method: "GET"
    })
    .then(res => res.json())
    .then(res => res['kakao_oauth_url']);

    const newWindow = openWindowPopup(url, "카카오톡 로그인");

    const checkConnect = setInterval(function() {
        if (!newWindow || !newWindow.closed) return;
        clearInterval(checkConnect);

        if(getCookie('logined') === 'true') {
            window.location.reload();
        } else {
            document.querySelector("#loading").classList.add('display_none');
        }
    }, 1000);
}

const redirectPage = () => {
    const pathname = window.location.pathname;
    if (pathname === '/oauth') {
        window.opener.location.reload();  // 메인 페이지를 리로드
        window.close();  // 팝업 창 닫기
    }
}

const autoLogin = async () => {
    let data;
    try {
        data = await fetch("/userinfo", {
            headers: { "Content-Type": "application/json" },
            method: "GET"
        })
        .then(res => res.json());
    } catch (error) {
        console.log(`Error fetching user info: ${error}`);
        return;
    }

    if (data.msg) {
        if (data.msg === `Missing cookie "access_token_cookie"`) {
            console.log("자동로그인 실패");
        } else if (data.msg === `Token has expired`) {
            console.log("Access Token 만료");
            refreshToken();
        }
    } else {
        console.log("자동로그인 성공");
        updateUserInterface(data);
    }
}

const refreshToken = async () => {
    let data;
    try {
        data = await fetch("/token/refresh", {
            headers: { "Content-Type": "application/json" },
            method: "GET"
        })
        .then(res => res.json());
    } catch (error) {
        console.log(`Error refreshing token: ${error}`);
        return;
    }

    if (data.result) {
        console.log("Access Token 갱신");
        autoLogin();
    } else {
        handleTokenExpiry(data.msg);
    }
}

const onLogout = async () => {
    let data;
    try {
        data = await fetch("/token/remove", {
            headers: { "Content-Type": "application/json" },
            method: "GET"
        })
        .then(res => res.json());
    } catch (error) {
        console.log(`Error logging out: ${error}`);
        return;
    }

    if (data.result) {
        console.log("로그아웃 성공");
        alert("정상적으로 로그아웃이 되었습니다.");
        window.location.reload();
    } else {
        console.log("로그아웃 실패");
    }
}

const getCookie = (cookieName) => {
    let cookieValue = null;
    if(document.cookie){
        let array = document.cookie.split((escape(cookieName) + '='));
        if(array.length >= 2){
            let arraySub = array[1].split(';');
            cookieValue = unescape(arraySub[0]);
        }
    }
    return cookieValue;
}

const updateUserInterface = (data) => {
    const nickname = document.querySelector("#nickname");
    const thumnail = document.querySelector("#thumnail");

    nickname.textContent = `${data.nickname}`;
    thumnail.src = data.profile;

    document.querySelector('#kakao').classList.add('display_none');
    document.querySelector('#logout').classList.remove('display_none');
    nickname.classList.remove('display_none');
    thumnail.classList.remove('display_none');
}

const handleTokenExpiry = (msg) => {
    if (msg === `Token has expired`) {
        console.log("Refresh Token 만료");
        resetLoginState();
        onKakao();
    } else {
        fetch("/token/remove", {
            headers: { "Content-Type": "application/json" },
            method: "GET"
        });
        alert("로그인을 다시 해주세요!");
        resetLoginState();
    }
}

const resetLoginState = () => {
    document.querySelector('#kakao').classList.remove('display_none');
    document.querySelector('#logout').classList.add('display_none');
    document.querySelector("#nickname").classList.add('display_none');
    document.querySelector("#thumnail").classList.add('display_none');
}

init();
