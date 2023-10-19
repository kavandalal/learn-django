import { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
	const [callAPI, setCallAPI] = useState(false);
	const [allRoutes, setAllRoutes] = useState([]);
	const [updateData, setUpdateData] = useState({ type: 'add', data: { id: '', identifier: '', link: '' } });

	useEffect(() => {
		getRoutes();
	}, [callAPI]);

	const getRoutes = async () => {
		const res = await axios.get('/api/data/');
		if (!res?.data?.ok) {
			console.error(res?.data);
			return false;
		}
		const packet = res?.data?.packet;
		setAllRoutes(packet);
		return true;
	};

	const handleChange = (e) => {
		const { name, value } = e.target;
		setUpdateData((prev) => ({
			...prev,
			data: {
				...prev.data,
				[name]: value,
			},
		}));
	};

	const handleSubmit = async (e) => {
		e.preventDefault();

		const sendData = { link: updateData?.data?.link, identifier: updateData?.data?.identifier };
		const url = '/api/create/';
		let type = 'post';
		if (updateData?.type === 'edit') {
			type = 'patch';
			sendData.id = updateData?.data?.id;
		}
		const res = await axios[type](url, sendData);
		if (!res?.data?.ok) {
			console.error(res?.data);
			return false;
		}
		setCallAPI((prev) => !prev);
		return true;
	};

	const handleEdit = (id) => {
		const editData = allRoutes.filter((i) => i?.id === id)[0];
		setUpdateData((prev) => ({
			...prev,
			type: 'edit',
			data: { ...prev.data, id, identifier: editData?.identifier, link: editData?.link },
		}));
	};

	const handleDelete = async (id) => {
		const res = await axios.delete(`/api/delete/${id}`);
		if (!res?.data?.ok) {
			console.error(res?.data);
			return false;
		}

		setCallAPI((prev) => !prev);
		return true;
	};

	// Get the CSRF token from the cookie
	const csrfToken = document?.cookie
		?.split('; ')
		?.find((row) => row.startsWith('csrftoken='))
		?.split('=')[1];

	// Include the CSRF token in the headers
	axios.defaults.xsrfCookieName = 'csrftoken'; // Ensure this matches your Django CSRF cookie name
	axios.defaults.xsrfHeaderName = 'X-CSRFToken';
	axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

	return (
		<div className='App'>
			<div>
				<h3>All Routes</h3>
				{/* {JSON.stringify(allRoutes)} */}
				<table>
					<thead>
						<th>index</th>
						<th>identifier</th>
						<th>link</th>
						<th>action</th>
					</thead>
					<tbody>
						{allRoutes?.map((i) => (
							<tr>
								<td>{i?.id}</td>
								<td>{i?.identifier}</td>
								<td>{i?.link}</td>
								<td>
									<button type='button' onClick={() => handleEdit(i?.id)}>
										Edit
									</button>
									<button type='button' onClick={() => handleDelete(i?.id)}>
										Delete
									</button>
								</td>
							</tr>
						))}
					</tbody>
				</table>
			</div>
			<hr />
			<div>
				<h3>Add Route</h3>
				<form onSubmit={handleSubmit} action=''>
					<input
						type='text'
						value={updateData?.data?.identifier}
						name={'identifier'}
						onChange={handleChange}
						placeholder='Identifier'
					/>
					<input type='text' value={updateData?.data?.link} name={'link'} onChange={handleChange} placeholder='Link' />
					<button type='submit'>Submit</button>
				</form>
			</div>
		</div>
	);
}

export default App;
