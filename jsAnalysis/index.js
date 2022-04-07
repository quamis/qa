onSubmit = function (event) {
    let hashes = computeHashes(input.value);

    $('#length').html(hashes.length);

    let friendlySortedLetters = hashes.sortedLetters.replaceAll(/[\s\r\n]/g, '');
    let maxLen = 60;
    $('#sortedLetters').html(
        friendlySortedLetters.length<maxLen?friendlySortedLetters:(friendlySortedLetters.substr(0, maxLen-3)+"...")
    );

    $('#crc16').html(hashes.crc16);
    $('#crc32').html(hashes.crc32);
    $('#md5').html(hashes.md5);
    $('#sha1').html(hashes.sha1);
    $('#sha256').html(hashes.sha256);

    $('#stats').html(JSONSyntaxHighlight(hashes));

    $('#binnedLettersCompressed').html(JSONSyntaxHighlight(hashes.binnedLettersCompressed));

    $('#input').attr('data-hashes', JSON.stringify(hashes));

    if (event) {
        event.preventDefault();
    }
    return false;
}


computeHashes = function (text) {
    let ret = {
        text:           '',
        length:         0,
        sortedLetters:  '',
        binnedLettersArr: [],
        binnedLettersCompressed: {
            missingLetter: '',
            missingCount: 0,
            text: '',
            length: 0
        },

        crc16:  '',
        crc32:  '',
        md5:    '',
        sha1:   '',
        sha256: '',
    };

    if (!text) {
        return ret;
    }

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

    ret.text= text;
    ret.length= text.length;
    ret.sortedLetters= lettersArr.join('');
    ret.binnedLettersArr= binnedLettersArr;
    ret.binnedLettersCompressed= {
        missingLetter: binnedLettersArr[0].letter,
        missingCount: text.length - binnedLettersCompressedText.length,
        text: binnedLettersCompressedText,
        length: binnedLettersCompressedText.length
    };

    ret.crc16= crc16(text);
    ret.crc32= crc32(text);
    ret.md5= md5(text);
    ret.sha1= sha1(text);
    ret.sha256= sha256(text);

    return ret;
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
        }
        else if (/true|false/.test(match)) {
            cls = 'boolean';
        }
        else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}