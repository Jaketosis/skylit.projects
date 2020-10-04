const express = require('express')
var path = require('path');
const cors = require('cors')
const bodyParser = require('body-parser')
const port = 3000
const { database } = require('./src/database')
const db = require('./queries')
var aws = require('aws-sdk');


const Sequelize = require('sequelize')
const sequelize = new Sequelize(
    'postgres',
    'jakemarsh',
    'Sephiroth!1',
    {
      host:'database-2.c2xa1utqjm6r.us-east-2.rds.amazonaws.com',
        dialect: 'postgres',
    },
  );
const app = express()

app.set('views', path.join(__dirname, 'views'));
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

app.use(bodyParser.json())
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
)

app.use(cors())

function clientErrorHandler (err, req, res, next) {
  if (req.xhr) {
     res.status(500).send({ error: 'Something failed!' })
   } else {
     next(err)
  }
}

app.use(clientErrorHandler);
// const links = await Link.findAll();
// console.log(links.every(user => link instanceof Link))
// console.log(Link === sequelize.models.Link);

sequelize

.authenticate()

.then(() => {

console.log('Connection has been established successfully.');

})

.catch(err => {

console.error('Unable to connect to the database:', err);

});
app.use('/services', require('./src/services'))
app.get('/',function (req,res){
  res.render('gallery')
})
database.sync().then(() => {
  app.listen(port, () => {
    console.log(`Listening on port ${port}`);
    

  })
})


//old
// app.get('/',(request, response)=>{
//     response.json({info:"Node baybay"})
// })

// app.listen(port, () => {
//     console.log(`App running on port ${port}.`)
//   })



