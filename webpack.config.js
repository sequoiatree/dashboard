const path = require('path');

module.exports = {
  mode: 'production',
  entry: {
    common: [
      './src/scripts/init.js',
    ],
    index: [
      './src/scripts/index.js',
    ]
  },
  output: {
    path: path.resolve('./static/scripts'),
    publicPath: '/static/scripts/',
    filename: '[name].js',
  },
};
