import('./init.js');


try {
    switch (location.pathname) { 
        case '/chat/index/':
            import('./pages/index.js');
            break;
        case '/chat/archive/':
            import('./pages/archive.js');
            break; 
    }
} catch (error) {
    console.error(error);
}
