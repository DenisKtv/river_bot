$(document).ready(function() {
    $('body').on('copy', function(e) {
        var selectedText = window.getSelection().toString();
        if (selectedText.length > 0) {
            var pageUrl = window.location.href;
            var citation = '\n\nИсточник: ' + pageUrl;
            var clipboardData = e.originalEvent.clipboardData || window.clipboardData;
            clipboardData.setData('text', selectedText + citation);
            e.preventDefault();
        }
    });
});
