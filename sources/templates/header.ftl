<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8"/>
    <title><#if (content.title)??><#escape x as x?xml>${content.title}</#escape><#else>AguasNegras</#if></title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="AguasNegras, tecnología, programación y Java">
    <meta name="author" content="Agustín Ventura">
    <meta name="keywords" content="Programación, Java">
    <meta name="generator" content="JBake">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    <link rel="stylesheet" href="<#if (content.rootpath)??>${content.rootpath}<#else></#if>css/aguasnegras.css"/>
    <link rel="shortcut icon" href="<#if (content.rootpath)??>${content.rootpath}<#else></#if>favicon.ico">
    <script src="https://kit.fontawesome.com/64e1074656.js" crossorigin="anonymous"></script>
  </head>
  <body>
    <header>
      	<#include "menu.ftl">
    </header>
