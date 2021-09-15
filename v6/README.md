run one test:
    reset && php -f ./generate-hash.php autoGenerateHash=autoGenerateHash_v2 action=autoRebuildStr

Try to remove one letter at a time, and rebuild the string without that letter, and also return a hash & a length difference