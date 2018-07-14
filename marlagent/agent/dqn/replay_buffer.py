import random
import numpy as np

class ReplayBuffer:
    """
    Replay Buffer stores the past obervations along with actions
    performed and the reward obtained after performing
    those actions.

    """

    def __init__(self, size, n_features):

        self.size = size
        self.n_features = n_features

        self.idx = 0
        self.num_in_buffer = 0

        self.obs = None
        self.action = None
        self.reward = None


    def store_transition(self, state, action, reward):

        if self.obs is None:
            self.obs        = np.empty([self.size, self.n_features],        dtype=np.float32)
            self.action     = np.empty([self.size],                         dtype=np.str)
            self.reward     = np.empty([self.size],                         dtype=np.float32)


        self.obs[self.idx] = state
        self.action[self.idx] = action['action']
        self.reward[self.idx] = reward

        # set the next idx
        # starts from 1st position and overwrites if buffer full
        self.idx = (self.idx + 1) % self.size

        # number of elements in the buffer.
        # if the buffer is full then the size of buffer is the number of elements present
        self.num_in_buffer = min(self.size, self.num_in_buffer + 1)


    def reset(self):
        self.idx = 0
        self.obs = np.empty([self.size, self.n_features], dtype=np.float32)
        self.action = np.empty([self.size], dtype=np.str)
        self.reward = np.empty([self.size], dtype=np.float32)


    def sample(self, batch_size):
        """Sample `batch_size` different transitions.
        i-th sample transition is the following:
        when observing `obs_batch[i]`, action `act_batch[i]` was taken,
        after which reward `rew_batch[i]` was received and subsequent
        observation  next_obs_batch[i] was observed, unless the epsiode
        was done which is represented by `done_mask[i]` which is equal
        to 1 if episode has ended as a result of that action.
        Parameters
        ----------
        batch_size: int
            How many transitions to sample.
        Returns
        -------
        obs_batch: np.array
            Array of shape
            (batch_size, img_c * frame_history_len, img_h, img_w)
            and dtype np.uint8
        act_batch: np.array
            Array of shape (batch_size,) and dtype np.int32
        rew_batch: np.array
            Array of shape (batch_size,) and dtype np.float32
        next_obs_batch: np.array
            Array of shape
            (batch_size, img_c * frame_history_len, img_h, img_w)
            and dtype np.uint8
        done_mask: np.array
            Array of shape (batch_size,) and dtype np.float32
        """

        # Extract the radom indexes of batch_size from the number of elements in the buffer
        idxes = sample_n_unique(lambda: random.randint(0, self.num_in_buffer - 2), batch_size)

        obs = np.concatenate([ self.obs[idx] for idx in idxes], 0)
        next_obs = np.copy(obs[1:, :])
        reward = np.concatenate([self.reward[idx] for idx in idxes],0)

        return obs[:-1, :], next_obs, reward



def sample_n_unique(sampling_f, n):
    """Helper function. Given a function `sampling_f` that returns
    comparable objects, sample n such unique objects.
    """
    res = []
    while len(res) < n:
        candidate = sampling_f()
        if candidate not in res:
            res.append(candidate)
    return res