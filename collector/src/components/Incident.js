import React from 'react'
import axios from 'axios'
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react"
import { Col, Container, Row, Button, Image, Form } from 'react-bootstrap';
import { useNavigate } from "react-router-dom";


export default function Incident() {

  let params = useParams();
  const url = "http://127.0.0.1:5000/incident/" + params.incidentId
  const [evidences, setEvidences] = useState(null)
  let navigate = useNavigate()


  useEffect(() => {
    axios.get(url).then(response => {
      setEvidences(response.data)
      console.log(response.data)
    })
  }, [url])



  if (evidences) {
    return (
      <Container fluid>
      <Row className='m-3'>
          <Col className='d-flex justify-content-end'>
              <Button variant="success" onClick={() => navigate('/incident/' + params.incidentId + '/createEvidence')}>New Evidence</Button>
          </Col>
      </Row>
        {evidences.map((evidence) =>
        <>
          <Row className='m-5'>
            <Col xs="6">
                <Row>
                  <Col>
                    <div>Date: {evidence.datetime}</div>
                    <div>Description: {evidence.description}</div>
                    <div>Host: {evidence.host}</div>
                    <div>Host Type: {evidence.host_type}</div>
                  </Col>
                </Row>
            </Col>
            <Col xs="6">
              <Image src={evidence.image_path} fluid></Image>
            </Col>
          </Row>
          <hr></hr>
        </>
        )}
        <Row className='mt-5'>
            <Col className='mt-5'>
                <Row>
                    <Col>
                        <Form.Group className="mb-3">
                            <Form.Label>Date</Form.Label>
                            <Form.Control name='date' type="date" placeholder="" />
                        </Form.Group>
                    </Col>
                    <Col>
                        <Form.Group className="mb-3">
                            <Form.Label>Time</Form.Label>
                            <Form.Control name='time' type="time" placeholder="" />
                        </Form.Group>
                    </Col>
                    <Col>
                        <Form.Group>
                            <Form.Label>Host</Form.Label>
                            <Form.Control name="host" type="text" size='md' ></Form.Control>
                        </Form.Group>
                    </Col>
                    <Col>
                    <Form.Group>
                        <Form.Label>Host Type</Form.Label>
                        <Form.Control name="host_type" type="text" size='md' ></Form.Control>
                    </Form.Group>
                    </Col>
                </Row>
                <Row>
                  <Col>
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
                  </Col>
                  <Col>
                    <Form.Group>
                        <Form.Label>Evidence</Form.Label>
                        <Form.Control type="file" size='md'></Form.Control>
                    </Form.Group>
                  </Col>
                  <Col>
                    <Form.Group>
                        <Form.Label>Description</Form.Label>
                        <Form.Control name="description" type="text" size='md' ></Form.Control>
                    </Form.Group>
                  </Col>
                </Row>
            </Col>
            <Row className='mt-5'>
                <Col className="d-grid d-md-none">
                    <Button variant="primary" type="submit" size="lg">Create Evidence</Button>
                </Col>
                <Col className="d-none d-md-flex">
                    <Button variant="primary" type="submit">Create Evidence</Button>
                </Col>
            </Row>
        </Row>
      </Container>
    )
  }
  else
    return (
      <div>Loading ...</div>
    )
}
