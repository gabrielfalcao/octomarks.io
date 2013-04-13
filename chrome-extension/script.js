// $('ul.pagehead-actions .watch-button-container').after('<li><a class="minibutton"><span>Bookmark</span></a></li>');

var li = document.createElement('li');
li.setAttribute('class', 'bookmark');
var a = document.createElement('a');
a.setAttribute('class', 'minibutton');
var span = document.createElement('span');
var text = document.createTextNode('Bookmark');

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
  chrome.extension.sendRequest(toggle_params, updateBookmarkButton);
};

// Is this page a bookmark?
var is_bookmark_params = params;
is_bookmark_params.query = 'isBookmark';
chrome.extension.sendRequest(is_bookmark_params, function(response) {
  if (response.is_bookmark) {
    text.nodeValue = "Already bookmarked!";
  }
  li.appendChild(a).appendChild(span).appendChild(text);
  // Insert Bookmark button into DOM
  var watch = document.getElementsByClassName('subscription')[0];
  var parentNode = watch.parentElement;
  parentNode.insertBefore(li, watch);

  updateBookmarkButton(response);
});

// Update 'Bookmark' button on page depending on response object
function updateBookmarkButton(response) {
  if (response.is_bookmark) {
    bookmark = response.bookmark;
    document.getElementsByClassName('bookmark')[0].firstChild.firstChild.innerText = 'Already bookmarked!';
    document.getElementsByClassName('bookmark')[0].firstChild.setAttribute('title', response.link_url);
  } else {
    bookmark = false;
    document.getElementsByClassName('bookmark')[0].firstChild.firstChild.innerText = 'Bookmark';
    document.getElementsByClassName('bookmark')[0].firstChild.removeAttribute('title');
  }
}
