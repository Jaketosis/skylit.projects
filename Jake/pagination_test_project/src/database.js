const Sequelize = require('sequelize');

const database = new Sequelize({

    "username": "jakemarsh",
    "password": "Sephiroth!1",
    "database": "postgres",
    "host": "database-2.c2xa1utqjm6r.us-east-2.rds.amazonaws.com",
    "dialect": "postgres",
    operatorsAliases: Sequelize.Op

})
const ghlinks = database.define('ghlinks',{
    id: {type:Sequelize.STRING, primaryKey: true },
    sourcelink: {type:Sequelize.STRING},
    imglink: {type:Sequelize.STRING},
    pictureindex: {type:Sequelize.INTEGER},

})

module.exports= {

    ghlinks,
    database

}