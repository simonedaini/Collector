import React from 'react'
import axios from 'axios'
import { useEffect, useState } from "react"
import { Button, Card, Container, Row, Col } from 'react-bootstrap';
import { useNavigate } from "react-router-dom";

export default function Customers() {

    const url = "http://127.0.0.1:5000/customer"
    const [customers, setCustomers] = useState(null)
    let navigate = useNavigate()

    useEffect(() => {
    axios.get(url).then(response => {
        setCustomers(response.data)
    })
    }, [url])


    if (customers){  
        return (
            <Container fluid>
                <Row className='m-3'>
                    <Col className='d-flex justify-content-end'>
                        <Button variant="success" onClick={() => navigate('/customer/create')}>New Customer</Button>
                    </Col>
                </Row>
                <Row>
                    {customers.map((customer) =>
                        <Col className="d-flex justify-content-center">
                            <div>
                            <Card style={{ width: '18rem' }}>
                            <Card.Img variant="top" src={"/customers/" + customer.logo_path}/>
                            <Card.Body className="d-flex justify-content-center">
                                <Button onClick={() => navigate('/customer/' + customer.id)} variant="primary">{customer.name} Incidents</Button>
                            </Card.Body>
                            </Card>
                            </div>
                        </Col>
                    )}
                </Row>
            </Container>
            
        );
    }
    else {
        return (
            <Container fluid>
                <Row className='m-3'>
                    <Col>
                        <h3>No customers yet. Create one using the green button on the right!</h3>
                    </Col>
                    <Col className='d-flex justify-content-end'>
                        <Button variant="success" onClick={() => navigate('/customer/create')}>New Customer</Button>
                    </Col>
                </Row>
            </Container>
            
        )
    }

}
