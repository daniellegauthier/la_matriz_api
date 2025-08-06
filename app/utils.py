import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def generate_visualization(rgb_sequence, momentum, pipeline, input_phrase, filepath):
    mapper = pipeline.named_steps['semantic_mapper']
    fig = plt.figure(figsize=(15, 10))
    plt.suptitle(f"Color Sequence for: \"{input_phrase}\"", fontsize=16, y=0.98)

    ax1 = fig.add_subplot(211, projection='3d')
    r, g, b = zip(*rgb_sequence)
    ax1.plot(r, g, b, 'o-', linewidth=2, markersize=10)
    for i, (r_, g_, b_) in enumerate(rgb_sequence):
        ax1.scatter(r_, g_, b_, color=[r_/255, g_/255, b_/255], s=100)
        ax1.text(r_, g_, b_, f"{i+1}", fontsize=12)
    ax1.set_xlabel('Red (R)')
    ax1.set_ylabel('Green (G)')
    ax1.set_zlabel('Blue (B)')
    ax1.set_xlim(0, 255)
    ax1.set_ylim(0, 255)
    ax1.set_zlim(0, 255)

    ax2 = fig.add_subplot(212)
    for i, (r_, g_, b_) in enumerate(rgb_sequence):
        ax2.add_patch(plt.Rectangle((i, 0), 1, 1, color=[r_/255, g_/255, b_/255]))
        rgb_key = f"{r_}_{g_}_{b_}"
        words = mapper.rgb_to_words_map.get(rgb_key, [])[:2]
        if words:
            ax2.text(i + 0.5, 1.1, ", ".join(words), ha='center', va='bottom', fontsize=10, rotation=45)
        if i < len(momentum):
            m = momentum[i]['magnitude'] / 255
            ax2.add_patch(plt.Rectangle((i + 0.9, 0), 0.1, m, color='red', alpha=0.7))
    ax2.set_xlim(0, len(rgb_sequence))
    ax2.set_ylim(0, 2)
    ax2.set_title('Color Sequence with Semantic Words and Momentum')
    ax2.set_xlabel('Sequence Position')
    ax2.set_yticks([])

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.savefig(filepath)
    plt.close()


def generate_color_sequence(seed_words, word_to_rgb_map, semantic_df, length=6, coherence=0.7):
    import random
    import numpy as np

    rgb_sequence = []
    seed_rgbs = [word_to_rgb_map[word] for word in seed_words if word in word_to_rgb_map]
    current_rgb = random.choice(seed_rgbs) if seed_rgbs else tuple(semantic_df.sample(1)[['R', 'G', 'B']].values[0].astype(int))
    rgb_sequence.append(current_rgb)

    for _ in range(1, length):
        if random.random() < coherence:
            variation = random.randint(10, 50)
            new_rgb = tuple(np.clip([current_rgb[i] + random.randint(-variation, variation) for i in range(3)], 0, 255))
            current_rgb = tuple(semantic_df.iloc[((semantic_df[['R', 'G', 'B']] - new_rgb)**2).sum(1).idxmin()][['R', 'G', 'B']].astype(int))
        else:
            current_rgb = tuple(semantic_df.sample(1)[['R', 'G', 'B']].values[0].astype(int))
        rgb_sequence.append(current_rgb)
    return rgb_sequence


def calculate_momentum(rgb_sequence):
    import numpy as np
    momentum = []
    for i in range(1, len(rgb_sequence)):
        prev_rgb, curr_rgb = rgb_sequence[i-1], rgb_sequence[i]
        direction = [curr_rgb[j] - prev_rgb[j] for j in range(3)]
        magnitude = np.linalg.norm(direction)
        norm_direction = [d / magnitude if magnitude > 0 else 0 for d in direction]
        momentum.append({
            'distance': magnitude,
            'direction': direction,
            'normalized_direction': norm_direction,
            'magnitude': magnitude
        })
    return momentum
