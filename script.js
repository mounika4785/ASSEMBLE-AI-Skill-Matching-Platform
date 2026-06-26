// 🔥 Firebase Config
const firebaseConfig = {
  apiKey: "AIzaSyAP-cSKtHdNzOI7U1JFibCAxAPJ0Ed3TFA",
  authDomain: "assembleproject2026.firebaseapp.com",
  projectId: "assembleproject2026"
};

// 🔥 Initialize Firebase
firebase.initializeApp(firebaseConfig);

// 🔥 Connect Firestore
const db = firebase.firestore();


// ✅ FETCH USERS FROM FIREBASE
async function getStudentsFromDB() {
  const snapshot = await db.collection("users").get();

  let students = [];

  snapshot.forEach(doc => {
    const data = doc.data();

    students.push({
      name: data.name || data.username || "Unknown",
      skills: data.skills || [],
      interests: data.interests || [],
      skill_levels: data.skill_levels || {},
      achievements: data.achievements || []
    });
  });

  return students;
}


// ✅ MAIN FUNCTION
async function getMatches() {

  console.log("Button clicked");

  // 🔹 Get input
  const input = document.getElementById("skillInput").value;

  if (!input.trim()) {
    alert("Please enter skills");
    return;
  }

  // 🔥 Convert input → array
  const skillsArray = input
    .split(",")
    .map(skill => skill.trim().toLowerCase())
    .filter(skill => skill !== "");

  try {

    // 🔥 Get students from Firebase
    const studentsData = await getStudentsFromDB();

    console.log("Students from Firebase:", studentsData);

    // 🔥 Opportunity data
    const opportunityData = {
      required_skills: skillsArray,
      description: input
    };

    // 🔥 Send to Flask AI
    const response = await fetch("http://127.0.0.1:5000/match", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        students: studentsData,
        opportunity: opportunityData
      })
    });

    if (!response.ok) {
      throw new Error("Server error");
    }

    const data = await response.json();

    console.log("AI Response:", data);

    // 🔥 Display results
    let resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "";

    data.forEach((user, index) => {
      resultDiv.innerHTML += `
        <div class="card ${index === 0 ? 'top' : ''}">
          
          <h3>${index === 0 ? "🏆 Top Candidate<br>" : ""}${user.name}</h3>
          
          <p class="score">
            Match Score: ${Math.round(user.score * 100)}%
          </p>
          
          <p class="missing">
            Missing Skills: ${
              user.missing_skills && user.missing_skills.length
                ? user.missing_skills.join(", ")
                : "None"
            }
          </p>

          <p class="achievements">
            Achievements: ${
              user.achievements && user.achievements.length
                ? user.achievements.join(", ")
                : "None"
            }
          </p>

        </div>
      `;
    });

  } catch (error) {
    console.error("ERROR:", error);
    alert("Error connecting to server or Firebase");
  }
}