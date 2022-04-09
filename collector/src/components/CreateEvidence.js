import axios from 'axios';
import React, { useState } from 'react'
import { Container, Form, Row, Col, Button } from 'react-bootstrap';
import { useParams } from 'react-router-dom';


export default function CreateCustomer() {

    let params = useParams()
    const [base64, setBase64] = useState(null)

    const [formValue, setFormValue] = useState({
        incidentId: params.incidentId,
        datetime: "",
        killchain: "",
        host: "",
        host_type: "",
        image: "",
        description: ""
    });

    const imageChange = (event) => {
        let image = event.target.files[0]
        let reader = new FileReader()
        reader.readAsDataURL(image)
        reader.onload = function () {
            setBase64(reader.result)
        }
    }

    const handleChange = (event) => {
        setFormValue({
          ...formValue,
          [event.target.name]: event.target.value
        });
      }

    const handleSubmit = (event) => {
        const data = {
            incidentId: params.incidentId,
            datetime: formValue.date + " " + formValue.time,
            killchain: formValue.killchain,
            host: formValue.host,
            host_type: formValue.host_type,
            image: base64,
            description: formValue.description
        }
        
        console.log(data)
        axios.post('http://127.0.0.1:5000/evidence/create', data)
            .then(response => console.log(response.status));
        event.preventDefault()
    }


    return (
        <Container>
            <div>{params.customerId}</div>
            <Form onSubmit={handleSubmit}>
                <Row className='mt-5'>
                    <h1>Create new Incident</h1>
                    <Col className='mt-5' xs="12" lg="6">
                        <Row>
                            <Col>
                                <Form.Group className="mb-3">
                                    <Form.Label>Date</Form.Label>
                                    <Form.Control name='date' type="date" placeholder="" onChange={handleChange}/>
                                </Form.Group>
                            </Col>
                            <Col>
                                <Form.Group className="mb-3">
                                    <Form.Label>Time</Form.Label>
                                    <Form.Control name='time' type="time" placeholder="" onChange={handleChange}/>
                                </Form.Group>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <Form.Group>
                                    <Form.Label>Host</Form.Label>
                                    <Form.Control name="host" type="text" size='md' onChange={handleChange}></Form.Control>
                                </Form.Group>
                            </Col>
                            <Col>
                            <Form.Group>
                                <Form.Label>Host Type</Form.Label>
                                <Form.Control name="host_type" type="text" size='md' onChange={handleChange}></Form.Control>
                            </Form.Group>
                            </Col>
                        </Row>
                        <Form.Group>
                            <Form.Label>Killchain</Form.Label>
                            <Form.Select>
                                <option>-</option>
                                <option>Recoinnessance</option>
                                <option>Weaponization</option>
                                <option>Delivery</option>
                                <option>Exploitation</option>
                                <option>Installation</option>
                                <option>Command and Control</option>
                                <option>Exfiltration</option>
                                <option>Action on Objectives</option>
                            </Form.Select>
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>Evidence</Form.Label>
                            <Form.Control type="file" size='md' onChange={imageChange}></Form.Control>
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>Description</Form.Label>
                            <Form.Control name="description" type="text" size='md' onChange={handleChange}></Form.Control>
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
