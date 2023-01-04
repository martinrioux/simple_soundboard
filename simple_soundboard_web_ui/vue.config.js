module.exports = {
    productionSourceMap: false,
    assetsDir: 'static',
    css: {
      extract: false
    },
    lintOnSave: true,
    filenameHashing: false,
    devServer: {
      proxy: {
        '/api': {
          target: 'http://localhost:4242/',
          changeOrigin: true,
        },
      },
    },
    configureWebpack: {
      output: {
        filename: "static/simple_soundboard/web_ui.js"
      }
    },
    chainWebpack: (config) => {
      config.optimization.delete('splitChunks');
      config.plugins.delete('preload');
      config.plugins.delete('prefetch');
      config.plugin('html').tap((args) => {
        args[0].title = 'Simple Soundboard';	// Replace your title here
        return args
      })
    }
  };
