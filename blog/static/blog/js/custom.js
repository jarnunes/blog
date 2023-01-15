let search = document.getElementById('inputSearch')
search.addEventListener('keypress', (e) => {
    if (e.code === 'Enter') {
        const searchValue = e.target.value;
        const queryString = `query=${searchValue}`
        getPosts(queryString);
    }
})

function getPosts(queryString) {
    const url = `/blog/${queryString === null ? '' : '?' + queryString}`
    console.log(url)
    fetch(url, {
        method: 'GET',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        }
    }).then(res => {
        let newurl = res['url'];
        window.history.pushState({path: newurl}, '', newurl);
        AjaxUtils.refresh('container');
    })
}
