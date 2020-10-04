const express = require('express');
const router = express.Router();

router.get('/',(req,res)=>res.send('LINKS'))

var express = require('express');
var router = express.Router();

const imglinkController = require('../controllers').imglinkcontroller

/* GET home page */

router.get('/',function(req, res, next) {
    res.render('index',{title:'Express'});
});

/* imglink router */
router.get('/api/imglink',imglinkController.list);
router.get('/api/imglink/:id',imglinkController.getById);
router.post('/api/imglink',imglinkController.add);
router.put('/api/imglink/:id',imglinkController.update);
router.delete('/api/imglink/:id',imglinkController.delete);

module.exports = router;