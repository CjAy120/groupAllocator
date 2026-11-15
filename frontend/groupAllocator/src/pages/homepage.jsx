import { useEffect, useState } from 'react';
import IndexForm from '../components/indexForm';
import Groups from '../components/groups';
import { findStudent, getGroups, registerStudent } from '../api';
import '../style.css';

function Homepage() {
  const [registrationResult, setRegistrationResult] = useState(null);
  const [lookupResult, setLookupResult] = useState(null);
  const [isRegistering, setIsRegistering] = useState(false);
  const [isLookingUp, setIsLookingUp] = useState(false);
  const [totalStudents, setTotalStudents] = useState(null);

  const refreshStudentCount = async () => {
    try {
      const groups = await getGroups();
      const count = groups.reduce(
        (total, group) => total + group.student_count,
        0
      );
      setTotalStudents(count);
    } catch {
      // The registration and lookup screens remain usable if this
      // optional footer statistic cannot be loaded.
    }
  };

  useEffect(() => {
    refreshStudentCount();
  }, []);

  const handleRegister = async ({ name, indexNumber }) => {
    setIsRegistering(true);
    setRegistrationResult(null);

    try {
      const response = await registerStudent({ name, indexNumber });
      const student = response.student;

      setRegistrationResult({
        status: 'success',
        student: {
          name: student.full_name,
          indexNumber: student.index_number,
        },
        group: {
          id: student.group_number,
        },
      });

      await refreshStudentCount();
    } catch (error) {
      let status = 'error';

      if (error.code === 'duplicate_index' || error.status === 409) {
        status = 'duplicate';
      } else if (error.code === 'allocation_error') {
        status = 'full';
      }

      setRegistrationResult({
        status,
        message: error.message,
      });
    } finally {
      setIsRegistering(false);
    }
  };

  const handleLookup = async (indexNumber) => {
    setIsLookingUp(true);
    setLookupResult(null);

    try {
      const response = await findStudent(indexNumber);
      const student = response.student;
      const group = response.group;

      setLookupResult({
        status: 'success',
        student: {
          name: student.full_name,
          indexNumber: student.index_number,
        },
        group: {
          id: group.number,
          capacity: group.capacity,
          members: group.members.map((member) => ({
            name: member.full_name,
            indexNumber: member.index_number,
          })),
        },
      });
    } catch (error) {
      if (error.status === 404 || error.code === 'student_not_found') {
        setLookupResult({ status: 'not-found' });
      } else {
        setLookupResult({
          status: 'error',
          message: error.message,
        });
      }
    } finally {
      setIsLookingUp(false);
    }
  };

  const closeLookup = () => setLookupResult(null);

  return (
    <main className="homepage">
      <header className="site-header">
        <div className="brand">
          <span>Student Allocation</span>
        </div>
      </header>

      <section className="hero-section">
        <span className="hero-label">STUDENT GROUP ALLOCATION</span>
        <h1>
          Find your place<br />
          <span>in a group.</span>
        </h1>
        <p>
          Register to receive your group assignment,
          or search for your existing allocation.
        </p>
      </section>

      <div className="portal-content">
        <IndexForm
          onRegister={handleRegister}
          disabled={isRegistering}
        />

        {registrationResult && (
          <div className={`registration-feedback ${registrationResult.status}`}>
            {registrationResult.status === 'success' ? (
              <>
                <span className="eyebrow">REGISTRATION COMPLETE</span>
                <h3>You have been assigned a group.</h3>
                <div className="registration-group">
                  <span>YOUR GROUP</span>
                  <strong>{registrationResult.group.id}</strong>
                </div>
                <p>
                  Welcome, {registrationResult.student.name}.
                  Your group assignment has been recorded.
                </p>
              </>
            ) : (
              <>
                <h3>Registration unsuccessful</h3>
                <p>{registrationResult.message}</p>
              </>
            )}
          </div>
        )}

        <Groups
          onLookup={handleLookup}
          lookupResult={lookupResult}
          onClose={closeLookup}
          isLookingUp={isLookingUp}
        />
      </div>

      <footer className="site-footer">
        <p>Student Group Allocation System</p>
        <span>
          {totalStudents === null ? 'Loading registrations…' : `${totalStudents} of 70 registrations`}
        </span>
      </footer>
    </main>
  );
}

export default Homepage;
