'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class imgLinkModel extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  };
  imgLinkModel.init({
    linkID: DataTypes.INTEGER,
    sourcelink: DataTypes.STRING,
    imglink: DataTypes.STRING,
    pictureindex: DataTypes.INTEGER
  }, {
    sequelize,
    modelName: 'imgLinkModel',
  });
  return imgLinkModel;
};