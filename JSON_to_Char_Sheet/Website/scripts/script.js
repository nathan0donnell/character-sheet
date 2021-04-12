function openTab(evt, id) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace("active", "");
  }
  var child, parent;
  child = document.getElementById(id);
  const scrollIntoViewOptions = {
    behavior: "smooth",
    block: "center",
  };
  document.getElementById(id).scrollIntoView(scrollIntoViewOptions);
  evt.currentTarget.className = "tablinks active";
}

function tabLoad() {
  var i, tabcontent;
  tabcontent = document.getElementsByClassName("tabcontent");
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    if (i === 0) {
      tablinks[i].className = "tablinks active";
    }
  }
}
