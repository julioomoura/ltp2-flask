function chamarURL(url, id, dados) {
 var xhttp = new XMLHttpRequest();
 xhttp.onreadystatechange = function() {
   if (this.readyState == 4 && this.status == 200) {
    document.getElementById(id).innerHTML = this.responseText;
   }
 };
 xhttp.open("POST", url, true);
 xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
 xhttp.send(dados);
 }