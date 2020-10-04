const Pool = require('pg').Pool
const pool = new Pool({
    user: 'jakemarsh',
    host: 'database-2.c2xa1utqjm6r.us-east-2.rds.amazonaws.com',
    database: 'postgres',
    password: 'Sephiroth!1',
    port: 5432,
})

const getUsers =(request,response)=>{
    pool.query('SELECT * FROM ghlinks',(error,results)=>{
        if (error) {
            throw error
        }
        response.status(200).json(results.rows)
    })
}
