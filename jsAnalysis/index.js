computeHashes = function(text) {
  let lettersArr = text.split('').sort();
  let binnedLetters = {};
  lettersArr.forEach(letter => {
    if (!binnedLetters[letter]) {
      binnedLetters[letter] = 1;
    }
    else {
      binnedLetters[letter]++;
    }
  });

  let binnedLettersArr = Object.keys(binnedLetters).map(letter => {
    return {
      letter: letter,
      count: binnedLetters[letter]
    };
  }).sort((a, b) => {
    return b.count - a.count;
  });
  let binnedLettersCompressedText = text.replaceAll(binnedLettersArr[0].letter, '');

  return {
    text:                       text,
    length:                     text.length,
    sortedLetters:              lettersArr.join(''),
    binnedLettersArr:           binnedLettersArr,
    binnedLettersCompressed:    {
      missingLetter: binnedLettersArr[0].letter,
      missingCount:  text.length - binnedLettersCompressedText.length,
      text:   binnedLettersCompressedText,
      length: binnedLettersCompressedText.length
    },

    md5:              md5(text),
  };
}


/**
 * @see https://stackoverflow.com/a/7220510/11301
 * @param {string} text
 * @returns {string}
 */
function JSONSyntaxHighlight(jsonObj) {
  let json = JSON.stringify(jsonObj, undefined, 2);
  json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
      var cls = 'number';
      if (/^"/.test(match)) {
          if (/:$/.test(match)) {
              cls = 'key';
          } else {
              cls = 'string';
          }
      } else if (/true|false/.test(match)) {
          cls = 'boolean';
      } else if (/null/.test(match)) {
          cls = 'null';
      }
      return '<span class="' + cls + '">' + match + '</span>';
  });
}