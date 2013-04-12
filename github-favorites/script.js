// $('ul.pagehead-actions .watch-button-container').after('<li><a class="minibutton"><span>Favorite</span></a></li>');

var li = document.createElement('li');
li.setAttribute('class', 'favorite');
var a = document.createElement('a');
a.setAttribute('class', 'minibutton');
var span = document.createElement('span');
var text = document.createTextNode('Favorite');

var params = {
  'url': document.location.href,
  'title': document.title
};
var bookmark = false;

li.onclick = function() {
  var toggle_params = params;
  toggle_params.query = 'toggle';
  if (bookmark) {
    toggle_params.id = bookmark.id;
  } else {
    toggle_params.id = false;
  }
  chrome.extension.sendRequest(toggle_params, updateFavoriteButton);
};

// Is this page a favorite?
var is_favorite_params = params;
is_favorite_params.query = 'isFavorite';
chrome.extension.sendRequest(is_favorite_params, function(response) {
  if (response.is_favorite) {
    text.nodeValue = "Favorited!";
  }
  li.appendChild(a).appendChild(span).appendChild(text);
  // Insert Favorite button into DOM
  var watch = document.getElementsByClassName('subscription')[0];
  var parentNode = watch.parentElement;
  parentNode.insertBefore(li, watch);

  updateFavoriteButton(response);
});

// Update 'Favorite' button on page depending on response object
function updateFavoriteButton(response) {
  if (response.is_favorite) {
    bookmark = response.bookmark;
    document.getElementsByClassName('favorite')[0].firstChild.firstChild.innerText = 'Favorited!';
    document.getElementsByClassName('favorite')[0].firstChild.setAttribute('title', 'Folder: ' + response.parent_folder_title);
  } else {
    bookmark = false;
    document.getElementsByClassName('favorite')[0].firstChild.firstChild.innerText = 'Favorite';
    document.getElementsByClassName('favorite')[0].firstChild.removeAttribute('title');
  }
}

/*
chrome.extension.onRequest.addListener(
  function(request, sender, sendResponse) {
    console.log(sender.tab ?
                "from a content script:" + sender.tab.url :
                "from the extension");
    
    
    sendResponse({
      farewell: "goodbye"
    });
    
    console.log('script.js', request, sender);
    
  }
);
*/