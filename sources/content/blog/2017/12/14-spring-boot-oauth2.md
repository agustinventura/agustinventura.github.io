title=Spring Boot 2, Spring Security 5 y OAuth 2
date=2017-12-14
type=post
tags=Java
status=draft
~~~~~~
Proyecto de ejemplo: https://github.com/spring-projects/spring-security/tree/5.0.0.RELEASE/samples/boot/oauth2login

Pasos:
1. Crear nueva aplicación en la consola de google (https://developers.google.com/identity/protocols/OpenIDConnect): https://console.developers.google.com/cloud-resource-manager?previousPage=%2F
2. Crear credenciales OAuth para la aplicación: https://console.developers.google.com/apis/credentials?project=...
3. Asegurarse de que en redirect URI se pone http://localhost:8080/login/oauth2/code/google
4. en application.properties establecer las propiedades spring.security.oauth2.client.registration.google.client-id y spring.security.oauth2.client.registration.google.client-secret
