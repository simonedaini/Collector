import axios from 'axios';
import React, { useState } from 'react'
import { Container, Form, Row, Col, Button } from 'react-bootstrap';
import { useParams } from 'react-router-dom';


export default function CreateCustomer() {

    let params = useParams()
    const today = new Date();
    const d = today.setDate(today.getDate()); 
    const defaultValue = new Date(d).toISOString().split('T')[0]
    const [formValue, setFormValue] = useState({
        customerId: null,
        date: defaultValue,
        type: "",
    });

    const handleChange = (event) => {
        setFormValue({
          ...formValue,
          [event.target.name]: event.target.value
        });
      }

    const handleSubmit = (event) => {

        const data = {
            customerId: params.customerId,
            date: formValue.date,
            type: formValue.type,
         }
        console.log(data)
        axios.post('http://127.0.0.1:5000/incident/create', data)
            .then(response => console.log(response.status));
        event.preventDefault()
    }



    return (
        <Container>
            <Form onSubmit={handleSubmit}>
                <Row className='mt-5'>
                    <h1>Create new Incident</h1>
                    <Col className='mt-5' xs="12" lg="6">
                        <Form.Group className="mb-3">
                            <Form.Label>Date</Form.Label>
                            <Form.Control name='date' type="date" placeholder="10/06/1193" defaultValue={defaultValue} onChange={handleChange}/>
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>Incident Type (optional)</Form.Label>
                            <Form.Control name="type" type="text" size='md' onChange={handleChange}></Form.Control>
                        </Form.Group>
                    </Col>
                    <Row className='mt-5'>
                        <Col className="d-grid d-md-none">
                            <Button variant="primary" type="submit" size="lg">Submit</Button>
                        </Col>
                        <Col className="d-none d-md-flex">
                            <Button variant="primary" type="submit">Submit</Button>
                        </Col>
                    </Row>
                </Row>
            </Form>
        </Container>
    )
}
