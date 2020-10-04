const express = require('express')

const { Service, ghlinks } = require('./database')

const router = express.Router()

router.get('/', async(req, res, next)=> {
    const page = req.query.page
    const inlimit = req.query.inlimit

    const startIndex = (page - 1) * inlimit
    const endIndex = page * inlimit

    const { userId } = req
    try{
        res.json(await ghlinks.findAll({
            limit:inlimit,
            offset:page * inlimit,
            attributes:['sourcelink','imglink','pictureindex','posttitle','mainpostedited','postdate'],
            where: { pictureindex:'/0' }

    }))} catch (error) {

        console.log(error)

    }

})

router.post('/', async(req, res, next)=>{

        try {

            const { userId } = req
            const { name } = req.body
            const { id } = await Service.create({ userId, name })
            res.json({success: true, id})

        } catch (error) {
            res.json({success: false, error: error.message})
        }

})

router.delete('/:id',async (req, res, next)=> {
    try {

        const { userd } = req
        const { id } = req.params
        if(await Service.dstroy({where : {userId, id}})) {
            res.json({success:true})
        } 

    } catch (error) {} res.json({success:false, error:'Invalid ID'})

})

module.exports = router