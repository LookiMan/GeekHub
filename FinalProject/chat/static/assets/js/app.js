import('./init.js');


try {
    const url = location.pathname;

    switch (true) { 
        case url.indexOf('/index/') !== -1:
            import('./pages/index.js');
            break;
        case url.indexOf('/archive/') !== -1:
            import('./pages/archive.js');
            break;
        case url.indexOf('/login/') !== -1:
            import('./pages/login.js');
            break; 
    }
} catch (error) {
    console.error(error);
}
