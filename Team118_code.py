import tkinter as tk
import random
import math
from tkinter import ttk, messagebox

# --- CONSTANTS ---
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

BULLET_RADIUS = 5
BALL_DENSITY = 1.0
MAX_LEVEL = 3
GAME_SPEED_MS = 20

class Bullet:
    """Represents the projectile fired from the cannon."""
    def __init__(self, canvas, x, y, vx, vy):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = BULLET_RADIUS
        self.id = canvas.create_oval(x-self.r, y-self.r, x+self.r, y+self.r, fill="#333333")

    def move(self):
        """Updates the bullet's position."""
        self.x += self.vx
        self.y += self.vy
        self.canvas.coords(self.id, self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r)


class Ball:
    """Represents the moving target balls."""
    def __init__(self, canvas, x, y, r, vx, vy, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = color
        self.score_value = int(r * 2)
        self.m = BALL_DENSITY * math.pi * (r ** 2) 

        self.id = canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill=color,
            outline="#333333",
            width=2
        )

    def move(self):
        """Updates the ball's position and handles wall bouncing."""
        self.x += self.vx
        self.y += self.vy

        if self.x - self.r < 0:
            self.x = self.r
            self.vx = abs(self.vx)
        elif self.x + self.r > CANVAS_WIDTH:
            self.x = CANVAS_WIDTH - self.r
            self.vx = -abs(self.vx)

        if self.y - self.r < 0:
            self.y = self.r
            self.vy = abs(self.vy)
        elif self.y + self.r > CANVAS_HEIGHT:
            self.y = CANVAS_HEIGHT - self.r
            self.vy = -abs(self.vy)

        self.canvas.coords(
            self.id,
            self.x - self.r, self.y - self.r,
            self.x + self.r, self.y + self.r
        )


class Game:
    def __init__(self, root):
        self.root = root
        root.title("HCI 418 Project: Shooting Balls Game")

        # 1. Game State Initialization
        self.balls = []
        self.bullets = []
        self.game_running = False
        self.score = 0
        self.level = 1
        self.level_transition = False
        self.start_time = 60
        self.time_left = self.start_time
        self.time_elapsed = 0
        self.game_loop_id = None
        self.timer_id = None
        self.colors = ["#e74c3c", "#3498db", "#2ecc71", "#f1c40f", "#9b59b6"]
        self.cannon_y = CANVAS_HEIGHT / 2

        # 2. UI Setup
        self._setup_ui()
        self._setup_controls()
        self._setup_keyboard()


        # 3. Initial Setup
        self.create_balls()
        self.update_cannon()
        self.update_score(0)

    def _setup_ui(self):
        """Sets up the main frames, canvas, and status bar."""
        self.main_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.control_frame = tk.Frame(self.main_frame, width=180, bg="#f5f7f9", padx=10, pady=10)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.control_frame.pack_propagate(False)

        self.canvas = tk.Canvas(self.main_frame, width=CANVAS_WIDTH,
                                 height=CANVAS_HEIGHT, bg="#cceaf7",
                                 borderwidth=0, highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.status_bar = tk.Frame(self.root, height=40, bg="#34495e")
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.score_label = tk.Label(self.status_bar, 
                                     text=f"Score: {self.score} | Level: {self.level} | Targets Left: 0 | Time: {self.time_left}s | Status: Ready",
                                     fg="white", bg="#34495e", font=("Arial", 12, "bold"),
                                     anchor="w", padx=10)
        self.score_label.pack(fill=tk.X, pady=5)
        
        # Cannon graphics setup
        self.cannon = self.canvas.create_rectangle(20, self.cannon_y-10,
                                                   40, self.cannon_y+10,
                                                   fill="#7f8c8d", outline="#34495e")

        self.barrel = self.canvas.create_line(40, self.cannon_y,
                                              90, self.cannon_y,
                                              width=5, fill="#2c3e50")

    def _setup_controls(self):
        """Sets up buttons and sliders in the control frame."""
        tk.Label(self.control_frame, text="GAME CONTROLS", font=("Arial", 10, "bold"), bg="#f5f7f9").pack(pady=(5, 5))

        self._create_colored_button("Start Game", self.start_game, "#2ecc71", "#27ae60").pack(pady=5)
        self._create_colored_button("Pause / Resume", self.pause_game, "#f39c12", "#e67e22").pack(pady=5)
        self._create_colored_button("Stop All", self.stop_game, "#e74c4c", "#c0392b").pack(pady=5)
        self._create_colored_button("Restart Game", self.restart_game, "#3498db", "#2980b9").pack(pady=5)
        self._create_colored_button("SHOOT!", self.shoot_bullet, "#9b59b6", "#8e44ad").pack(pady=(15, 10), ipady=5, fill=tk.X)

        tk.Label(self.control_frame, text="CANNON SETTINGS", font=("Arial", 10, "bold"), bg="#f5f7f9").pack(pady=(10, 5))

        tk.Label(self.control_frame, text="Angle (0-90°)", bg="#f5f7f9").pack()
        self.angle_slider = tk.Scale(self.control_frame, from_=0, to=90, orient="horizontal", length=160, command=self._update_cannon_on_slide)
        self.angle_slider.set(30)
        self.angle_slider.pack()

        tk.Label(self.control_frame, text="Barrel Length (Visual)", bg="#f5f7f9").pack()
        self.length_slider = tk.Scale(self.control_frame, from_=40, to=120, orient="horizontal", length=160, command=self._update_cannon_on_slide)
        self.length_slider.set(70)
        self.length_slider.pack()

        tk.Label(self.control_frame, text="Power/Strength (Speed)", bg="#f5f7f9").pack()
        self.power_slider = tk.Scale(self.control_frame, from_=5, to=20, orient="horizontal", length=160, command=self._update_cannon_on_slide)
        self.power_slider.set(10)
        self.power_slider.pack()

        tk.Label(self.control_frame, text="Vertical Position", bg="#f5f7f9").pack()
        self.pos_slider = tk.Scale(self.control_frame, from_=CANVAS_HEIGHT-50, to=50, length=160, command=self._update_cannon_on_slide)
        self.pos_slider.set(self.cannon_y)
        self.pos_slider.pack()
    def _setup_keyboard(self):
     """Keyboard shortcuts: Space = shoot, P = pause, Arrows = adjust cannon."""
     self.root.bind("<space>", lambda e: self.shoot_bullet())
     self.root.bind("<p>", lambda e: self.pause_game())

    # Adjust angle with arrows
     self.root.bind("<Up>", lambda e: self._adjust_angle(1))
     self.root.bind("<Down>", lambda e: self._adjust_angle(-1))

    # Adjust vertical cannon position
     self.root.bind("<Right>", lambda e: self._adjust_position(5))
     self.root.bind("<Left>", lambda e: self._adjust_position(-5))
    def _adjust_angle(self, change):
      new_angle = self.angle_slider.get() + change
      if 0 <= new_angle <= 90:
          self.angle_slider.set(new_angle)
          self.update_cannon()

    def _adjust_position(self, change):
     new_pos = self.pos_slider.get() + change
     if -50 <= new_pos <= CANVAS_HEIGHT + 50:
         self.pos_slider.set(new_pos)
         self.update_cannon()

   
    def _create_colored_button(self, text, command, bg, hover_bg):
        """Helper to create visually appealing buttons (HCI aesthetics)."""
        btn = tk.Button(self.control_frame, text=text, command=command, width=16, bg=bg, fg="white",
                         font=("Arial", 10, "bold"), relief="groove", cursor="hand2")
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    def update_score(self, points):
      self.score += points
    
      if self.game_running:
        status = "Running"
      elif len(self.balls) > 0:
        status = "Paused"
      else:
        status = "Ready"


      self.score_label.config(
        text=f"Score: {self.score} | Level: {self.level} | "
             f"Targets Left: {len(self.balls)} | Time: {self.time_left}s | Status: {status}")


        
    def update_status(self, status_message):
       self.score_label.config(
    text=f"Score: {self.score} | Level: {self.level} | "
         f"Targets Left: {len(self.balls)} | Time: {self.time_left}s | Status: {status_message}")



    def _update_cannon_on_slide(self, value=None): 
        """Handler function for slider update."""
        self.update_cannon()

    def update_cannon(self):
        """Updates cannon position, barrel geometry, and visual strength."""
        self.cannon_y = self.pos_slider.get()

        self.canvas.coords(self.cannon, 20, self.cannon_y-10, 40, self.cannon_y+10)

        angle_rad = math.radians(self.angle_slider.get())
        length = self.length_slider.get()
        power_val = self.power_slider.get() 
        
        barrel_width = 5 + (power_val - 5) * 7 / 15 

        x2 = 40 + length * math.cos(angle_rad)
        y2 = self.cannon_y - length * math.sin(angle_rad)

        self.canvas.coords(self.barrel, 40, self.cannon_y, x2, y2)
        self.canvas.itemconfig(self.barrel, width=barrel_width)


    def shoot_bullet(self):
        """Calculates bullet trajectory and creates a new bullet (Physics application)."""
        if not self.game_running:
            self.update_status("Game is Paused/Stopped - Press Start/Resume!")
            return

        angle_rad = math.radians(self.angle_slider.get())
        power = self.power_slider.get() 

        vx = power * math.cos(angle_rad)
        vy = -power * math.sin(angle_rad)

        length = self.length_slider.get()
        x_start = 40 + length * math.cos(angle_rad)
        y_start = self.cannon_y - length * math.sin(angle_rad)

        bullet = Bullet(self.canvas, x_start, y_start, vx, vy)
        self.bullets.append(bullet)
        self.update_status("Shot fired!")

    def update_time(self):
        if self.game_running:
            self.time_left -= 1

            if self.time_left <= 0:
                self.update_status("Time's up!")
                messagebox.showinfo("Game Over", "Time is up!")
                self.stop_game()
                return

            self.update_score(0)
            self.timer_id = self.root.after(1000, self.update_time)

    def start_game(self):
       self.level_transition = False

       self.time_left = max(15, 60 - (self.level - 1) * 5)

       if not self.game_running:
        self.game_running = True
        self.update_status("Running")

        # ADD THIS
        if not self.balls:
            self.create_balls()

        if self.timer_id is None:
            self.update_time()

        self.update_game()


    def pause_game(self):
        """Pauses or resumes the game loop and timer."""
        self.game_running = not self.game_running
        
        if self.game_running:
            self.update_status("Resumed")
            self.update_game()
            if self.timer_id is None:
                self.update_time()
        else:
            self.update_status("Paused")
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None 

    def stop_game(self):
        """Stops the game and clears all balls and bullets."""
        self.game_running = False
        
        if self.game_loop_id:
            self.root.after_cancel(self.game_loop_id)
            self.game_loop_id = None
            
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        for item in self.balls + self.bullets:
            self.canvas.delete(item.id)
            
        self.balls.clear()
        self.bullets.clear()
        
        self.score = 0
        self.level = 1
        self.time_left = self.start_time   
        self.level_transition = False      
  

        self.update_status("Stopped. Ready to restart.")

    def restart_game(self):
        """Restarts the game."""
        self.stop_game()
        self.create_balls()
        self.start_game()
        self.update_status("Restarted")

    def create_balls(self):
        """Creates new random balls on the canvas, scaling difficulty with level."""
        for ball in self.balls:
            self.canvas.delete(ball.id)
        self.balls.clear()
        
        count = 20 + (self.level - 1) * 2
        base_speed = 2 + (self.level * 0.5)

        for i in range(count):
            r = random.randint(20, 35)
            x = random.randint(150 + r, CANVAS_WIDTH - r) 
            y = random.randint(r, CANVAS_HEIGHT - r)

            speed = random.uniform(base_speed - 1, base_speed)
            angle = random.uniform(0, 2 * math.pi)
            
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)

            color = self.colors[i % len(self.colors)]
            ball = Ball(self.canvas, x, y, r, vx, vy, color)
            self.balls.append(ball)
        self.update_score(0)

    def check_bullet_collision(self):
        """Checks for bullet-ball collisions and out-of-bounds bullets, updating score."""
        balls_to_remove = []
        bullets_to_remove = []
        points_gained = 0

        for bullet in self.bullets:
            bullet_removed = False
            for ball in self.balls:
                dx = bullet.x - ball.x
                dy = bullet.y - ball.y
                distance = math.sqrt(dx*dx + dy*dy)

                if distance <= ball.r + BULLET_RADIUS: 
                    balls_to_remove.append(ball)
                    bullets_to_remove.append(bullet)
                    points_gained += ball.score_value
                    bullet_removed = True
                    break

            if not bullet_removed and (bullet.x < 0 or bullet.x > CANVAS_WIDTH or 
                                         bullet.y < 0 or bullet.y > CANVAS_HEIGHT):
                bullets_to_remove.append(bullet)

        for ball in set(balls_to_remove):
            if ball in self.balls:
                self.canvas.delete(ball.id)
                self.balls.remove(ball)

        for bullet in set(bullets_to_remove):
            if bullet in self.bullets:
                self.canvas.delete(bullet.id)
                self.bullets.remove(bullet)
                
        if points_gained > 0:
            self.update_score(points_gained)
            
        self._check_level_completion()


    def _check_level_completion(self):
       if len(self.balls) == 0 and self.game_running and not self.level_transition:
        self.level_up()


    def level_up(self):
    # Prevent double execution
     if self.level_transition:
        return
     self.level_transition = True

    # Stop old timer
     if self.timer_id:
        self.root.after_cancel(self.timer_id)
        self.timer_id = None

    # MAX LEVEL CHECK
     if self.level >= MAX_LEVEL:
        messagebox.showinfo("Congratulations!",
                            f"You completed all levels!\nFinal Score: {self.score}")
        self.game_running = False
        return

    # Increase level
     self.level += 1

    # Decrease time each level (minimum 15 seconds)
     self.time_left = max(15, 60 - (self.level - 1) * 5)

    # Update UI
     self.update_status("Level up!")

     messagebox.showinfo("Level Complete!", f"Starting Level {self.level}")

    # Create harder balls
     self.create_balls()

    # Resume game properly
     self.level_transition = False
     self.game_running = True
     self.update_game()
     self.update_time()



    def check_ball_collisions(self):
        """Handles elastic collision between balls (Physics application)."""
        num_balls = len(self.balls)
        for i in range(num_balls):
            for j in range(i + 1, num_balls):
                ball1 = self.balls[i]
                ball2 = self.balls[j]

                dx = ball1.x - ball2.x
                dy = ball1.y - ball2.y
                distance = math.sqrt(dx*dx + dy*dy)
                min_distance = ball1.r + ball2.r
                
                if distance < min_distance:
                    # Separate overlapping balls
                    overlap = min_distance - distance
                    nx = dx / distance
                    ny = dy / distance
                    
                    ball1.x += nx * overlap * 0.5
                    ball1.y += ny * overlap * 0.5
                    ball2.x -= nx * overlap * 0.5
                    ball2.y -= ny * overlap * 0.5
                    
                    # Tangent vector
                    tx = -ny
                    ty = nx
                    
                    # Velocity components along the normal (n) and tangent (t) axes
                    v1n = ball1.vx * nx + ball1.vy * ny
                    v1t = ball1.vx * tx + ball1.vy * ty
                    
                    v2n = ball2.vx * nx + ball2.vy * ny
                    v2t = ball2.vx * tx + ball2.vy * ty
                    
                    m1 = ball1.m
                    m2 = ball2.m
                    
                    # Calculate new normal velocities using 1D elastic collision formula
                    v1n_prime = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
                    v2n_prime = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)
                    
                    # Tangential velocities remain unchanged
                    v1t_prime = v1t
                    v2t_prime = v2t
                    
                    # Convert final velocities back to 2D (x, y) coordinates
                    ball1.vx = v1n_prime * nx + v1t_prime * tx
                    ball1.vy = v1n_prime * ny + v1t_prime * ty
                    
                    ball2.vx = v2n_prime * nx + v2t_prime * tx
                    ball2.vy = v2n_prime * ny + v2t_prime * ty


    def update_game(self):
        """The main game loop. Runs at a fixed interval (GAME_SPEED_MS)."""
        if not self.game_running:
            return

        for ball in self.balls:
            ball.move()

        for bullet in self.bullets:
            bullet.move()
            
        self.check_ball_collisions()
            
        self.check_bullet_collision()
        
        self.game_loop_id = self.root.after(GAME_SPEED_MS, self.update_game)

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()