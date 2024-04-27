function selectSystem(index){
    for (let i = 0; i < 14; i++){
        document.querySelector('.system' + i.toString()).style.display = 'none';
    }
    document.querySelector('.system' + index.toString()).style.display = 'block';
}