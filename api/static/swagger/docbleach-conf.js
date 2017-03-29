$(function () {
  hljs.configure({
    highlightSizeThreshold: 5000
  });

  // Pre load translate...
  if (window.SwaggerTranslator) {
    window.SwaggerTranslator.translate();
  }
  window.swaggerUi = new SwaggerUi({
    url: "/static/swagger.yaml",
    dom_id: "swagger-ui-container",
    supportedSubmitMethods: ['get', 'post', 'put', 'delete', 'patch'],
    onComplete: function (swaggerApi, swaggerUi) {
      if (window.SwaggerTranslator) {
        window.SwaggerTranslator.translate();
      }
    },
    onFailure: function (data) {
      log("Unable to Load SwaggerUI");
    },
    docExpansion: "full",
    jsonEditor: false,
    defaultModelRendering: 'schema',
    showRequestHeaders: false,
    validatorUrl: null
  });

  window.swaggerUi.load();

  function log() {
    if ('console' in window) {
      console.log.apply(console, arguments);
    }
  }
});