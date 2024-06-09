maybe use this to do dynamic subdomains?

<IfModule mod_proxy.c>
  SetEnvIf Host "^([^.]*).example.org$" SUBDOMAIN=$1
  ProxyPassInterpolateEnv On
  ProxyPass / https://${SUBDOMAIN}.hello.dev/ interpolate
  ProxyPassReverse / https://${SUBDOMAIN}.hello.dev/ interpolate
 </IfModule>